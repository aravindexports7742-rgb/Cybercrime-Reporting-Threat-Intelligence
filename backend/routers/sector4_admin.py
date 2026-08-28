from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database.connection import get_db
from backend.models.shared_models import User, Role
from backend.models.sector4_admin import (
    Incident, IncidentActivity, ResponseAction, Playbook, PlaybookStep, AuditLog, LoginHistory, SystemHealth
)
from backend.models.sector2_officer import Case, InvestigationActivity
from backend.models.sector1_victim import Complaint, VictimProfile, Notification
from backend.schemas.sector4_admin import (
    IncidentCreate, IncidentOut, IncidentUpdate,
    PlaybookCreate, PlaybookOut,
    AuditLogOut, LoginHistoryOut, SystemHealthOut,
    UserCreate, UserOut, UserUpdateRole, RoleOut
)
from backend.security.auth import get_current_user
from backend.security.rbac import get_role_checker
from backend.security.hashing import get_password_hash

router = APIRouter(prefix="/admin", tags=["Sector 4: Admin & Incident Response"])

allow_responder = get_role_checker(["Incident Responder", "Administrator"])
allow_admin = get_role_checker(["Administrator"])
# These monitoring pages are visible to Incident Responders in the UI. They
# receive read-only access; all administrative changes remain Admin-only.
allow_admin_read = get_role_checker(["Incident Responder", "Administrator"])

# ===================== Incidents =====================

@router.post("/incidents", response_model=IncidentOut, dependencies=[Depends(allow_responder)])
def create_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    if incident.case_id is not None and not db.query(Case).filter(Case.case_id == incident.case_id).first():
        raise HTTPException(status_code=404, detail="Linked case not found")

    new_incident = Incident(
        incident_reference=incident.incident_reference,
        case_id=incident.case_id,
        ioc_id=incident.ioc_id,
        responder_id=incident.responder_id,
        incident_type=incident.incident_type,
        description=incident.description,
        severity=incident.severity,
        status=incident.status
    )
    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)
    return new_incident

@router.get("/incidents", response_model=List[IncidentOut], dependencies=[Depends(allow_responder)])
def list_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).all()

@router.get("/incidents/{incident_id}", response_model=IncidentOut, dependencies=[Depends(allow_responder)])
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@router.put("/incidents/{incident_id}", response_model=IncidentOut, dependencies=[Depends(allow_responder)])
def update_incident(incident_id: int, incident_update: IncidentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    if incident_update.responder_id is not None:
        incident.responder_id = incident_update.responder_id
    if incident_update.severity is not None:
        incident.severity = incident_update.severity
    previous_status = incident.status
    if incident_update.status is not None:
        incident.status = incident_update.status
    if incident_update.description is not None:
        incident.description = incident_update.description

    # Log the activity
    activity = IncidentActivity(
        incident_id=incident_id,
        performed_by=current_user.user_id,
        action=f"Updated incident status to {incident.status}, severity to {incident.severity}"
    )
    db.add(activity)

    # A resolved response must be visible to the investigation officer and
    # victim.  Sector 4 closes the security incident; Sector 2 retains the
    # authority to perform the final legal/investigation case closure.
    if (
        previous_status != incident.status
        and incident.status in {"Resolved", "Closed"}
        and incident.case_id is not None
    ):
        linked_case = db.query(Case).filter(Case.case_id == incident.case_id).first()
        if linked_case and linked_case.status != "Closed":
            if linked_case.status != "Resolved":
                linked_case.status = "Resolved"
                db.add(InvestigationActivity(
                    case_id=linked_case.case_id,
                    officer_id=current_user.user_id,
                    action="Incident response completed",
                    result=(
                        f"Incident {incident.incident_reference} was marked {incident.status}. "
                        "Case is ready for final officer review and closure."
                    ),
                ))

            complaint = db.query(Complaint).filter(
                Complaint.complaint_id == linked_case.complaint_id
            ).first()
            if complaint and complaint.status not in {"Resolved", "Closed"}:
                complaint.status = "Resolved"
                profile = db.query(VictimProfile).filter(
                    VictimProfile.victim_id == complaint.victim_id
                ).first()
                if profile:
                    db.add(Notification(
                        user_id=profile.user_id,
                        complaint_id=complaint.complaint_id,
                        message=(
                            f"Response to your complaint has been completed. "
                            f"Case {linked_case.case_reference} is resolved and under final officer review."
                        ),
                        event_type="Incident Resolved",
                    ))

            db.add(AuditLog(
                user_id=current_user.user_id,
                action="Incident Resolution Synced",
                resource="cases",
                resource_id=str(linked_case.case_id),
            ))

    db.commit()
    db.refresh(incident)
    return incident


# ===================== Playbooks =====================

@router.post("/playbooks", response_model=PlaybookOut, dependencies=[Depends(allow_admin)])
def create_playbook(playbook: PlaybookCreate, db: Session = Depends(get_db)):
    new_playbook = Playbook(
        playbook_name=playbook.playbook_name,
        incident_type=playbook.incident_type,
        description=playbook.description
    )
    db.add(new_playbook)
    db.commit()
    db.refresh(new_playbook)
    
    for step in playbook.steps:
        new_step = PlaybookStep(
            playbook_id=new_playbook.playbook_id,
            step_order=step.step_order,
            step_description=step.step_description
        )
        db.add(new_step)
    
    db.commit()
    db.refresh(new_playbook)
    return new_playbook

@router.get("/playbooks", response_model=List[PlaybookOut], dependencies=[Depends(allow_responder)])
def list_playbooks(db: Session = Depends(get_db)):
    return db.query(Playbook).all()

@router.post("/incidents/{incident_id}/execute-playbook", dependencies=[Depends(allow_responder)])
def execute_playbook(incident_id: int, playbook_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    playbook = db.query(Playbook).filter(Playbook.playbook_id == playbook_id).first()
    
    if not incident or not playbook:
        raise HTTPException(status_code=404, detail="Incident or Playbook not found")
        
    action = ResponseAction(
        incident_id=incident_id,
        action_type="Playbook Execution",
        description=f"Executed playbook: {playbook.playbook_name}",
        performed_by=current_user.user_id
    )
    db.add(action)
    db.commit()

    # Audit log
    audit = AuditLog(
        user_id=current_user.user_id,
        action="Execute Playbook",
        resource="playbooks",
        resource_id=str(playbook_id)
    )
    db.add(audit)
    db.commit()

    return {"message": "Playbook executed successfully"}

# ===================== Users & Roles =====================

@router.get("/users", response_model=List[UserOut], dependencies=[Depends(allow_admin_read)])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/access-requests", dependencies=[Depends(allow_admin)])
def list_access_requests(db: Session = Depends(get_db)):
    """Lists public registrations that require administrator approval."""
    requests = db.query(User).filter(User.account_status == "Pending").all()
    return [{
        "user_id": user.user_id,
        "full_name": user.full_name,
        "email": user.email,
        "phone_number": user.phone_number,
        "requested_role": user.role.role_name,
        "created_at": user.created_at,
    } for user in requests]

@router.put("/access-requests/{user_id}", dependencies=[Depends(allow_admin)])
def decide_access_request(user_id: int, decision: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if decision not in {"approve", "reject"}:
        raise HTTPException(status_code=400, detail="Decision must be 'approve' or 'reject'")
    user = db.query(User).filter(User.user_id == user_id, User.account_status == "Pending").first()
    if not user:
        raise HTTPException(status_code=404, detail="Pending access request not found")
    user.account_status = "Active" if decision == "approve" else "Suspended"
    db.add(AuditLog(user_id=current_user.user_id, action=f"Access request {decision}", resource="users", resource_id=str(user.user_id)))
    db.commit()
    return {"message": f"Access request {decision}d.", "account_status": user.account_status}

@router.post("/users", response_model=UserOut, dependencies=[Depends(allow_admin)])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.role_name == user.role_name).first()
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role")
        
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
        
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        phone_number=user.phone_number,
        password_hash=get_password_hash(user.password),
        role_id=role.role_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/users/{user_id}/role", response_model=UserOut, dependencies=[Depends(allow_admin)])
def update_user_role(user_id: int, update: UserUpdateRole, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    role = db.query(Role).filter(Role.role_name == update.role_name).first()
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role")
        
    user.role_id = role.role_id
    db.commit()
    db.refresh(user)
    
    # Audit log
    audit = AuditLog(
        user_id=current_user.user_id,
        action="Change Role",
        resource="users",
        resource_id=str(user.user_id)
    )
    db.add(audit)
    db.commit()
    
    return user

@router.get("/roles", response_model=List[RoleOut], dependencies=[Depends(allow_admin_read)])
def list_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()

# ===================== Audit & Health =====================

@router.get("/audit-logs", response_model=List[AuditLogOut], dependencies=[Depends(allow_admin_read)])
def list_audit_logs(db: Session = Depends(get_db)):
    return db.query(AuditLog).order_by(AuditLog.event_time.desc()).limit(100).all()

@router.get("/login-history", response_model=List[LoginHistoryOut], dependencies=[Depends(allow_admin_read)])
def list_login_history(db: Session = Depends(get_db)):
    return db.query(LoginHistory).order_by(LoginHistory.event_time.desc()).limit(100).all()

@router.get("/system-health", response_model=List[SystemHealthOut], dependencies=[Depends(allow_admin_read)])
def get_system_health(db: Session = Depends(get_db)):
    return db.query(SystemHealth).order_by(SystemHealth.checked_at.desc()).limit(5).all()
