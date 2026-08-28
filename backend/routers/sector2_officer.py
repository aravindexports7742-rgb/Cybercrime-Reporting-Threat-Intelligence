from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database.connection import get_db
from backend.models.shared_models import User
from backend.models.sector1_victim import Complaint, Evidence, Notification
from backend.models.sector2_officer import Case, InvestigationNote, InvestigationActivity, Suspect, ChainOfCustody, AgencyCoordination, EvidenceAccessHistory
from backend.models.sector4_admin import AuditLog, Incident
from backend.schemas.sector2_officer import CaseResponse, CaseUpdate, InvestigationNoteCreate, InvestigationNoteResponse, InvestigationActivityCreate, InvestigationActivityResponse, SuspectCreate, SuspectResponse, CustodyEventCreate, CustodyEventResponse, AgencyCoordinationCreate, AgencyCoordinationResponse
from backend.security.auth import get_current_user
from backend.security.rbac import get_role_checker
import datetime

router = APIRouter(prefix="/cases", tags=["Sector 2: Officer Portal"])

allow_officer = get_role_checker(["Officer", "Administrator"])

@router.get("/", response_model=List[CaseResponse], dependencies=[Depends(allow_officer)])
def get_cases(db: Session = Depends(get_db)):
    return db.query(Case).all()

@router.get("/{case_id}", response_model=CaseResponse, dependencies=[Depends(allow_officer)])
def get_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.put("/{case_id}", response_model=CaseResponse, dependencies=[Depends(allow_officer)])
def update_case(case_id: int, updates: CaseUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    case = db.query(Case).filter(Case.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
        
    old_status = case.status
    old_priority = case.priority
    
    if updates.priority:
        case.priority = updates.priority
    if updates.status:
        case.status = updates.status
        if updates.status == "Closed" and case.closed_at is None:
            case.closed_at = datetime.datetime.utcnow()
    if old_status != case.status or old_priority != case.priority:
        db.add(InvestigationActivity(
            case_id=case.case_id,
            officer_id=current_user.user_id,
            action="Case status/priority updated",
            result=f"Status: {old_status} -> {case.status}; priority: {old_priority} -> {case.priority}",
        ))
        
    db.commit()
    db.refresh(case)
    
    # 1. Status Synchronization (Sector 2 -> Sector 1)
    if old_status != case.status:
        complaint = db.query(Complaint).filter(Complaint.complaint_id == case.complaint_id).first()
        if complaint:
            # Map statuses (Simplified mapping)
            complaint_status_map = {
                "New": "Submitted",
                "Under Review": "Under Review",
                "Assigned": "Assigned",
                "Investigation": "Investigation",
                "Action Taken": "Action Taken",
                "Resolved": "Resolved",
                "Closed": "Closed"
            }
            if case.status in complaint_status_map:
                complaint.status = complaint_status_map[case.status]
                db.commit()
                
            # Create notification for Victim using the correct users.user_id (not victim_profiles.victim_id)
            from backend.models.sector1_victim import VictimProfile
            profile = db.query(VictimProfile).filter(VictimProfile.victim_id == complaint.victim_id).first()
            if profile:
                notification = Notification(
                    user_id=profile.user_id,
                    complaint_id=complaint.complaint_id,
                    message=f"Your complaint status has been updated to '{case.status}'.",
                    event_type="Status Update"
                )
                db.add(notification)
                db.commit()

    # 2. Threat Escalation (Sector 2 -> Sector 4)
    if old_priority != "Critical" and case.priority == "Critical":
        incident = Incident(
            incident_reference=f"INC-CASE-{case.case_id}-{int(datetime.datetime.now().timestamp())}",
            case_id=case.case_id,
            incident_type="Escalated Case",
            description=f"Case {case.case_reference} escalated to Critical priority.",
            severity="Critical",
            status="Detected"
        )
        db.add(incident)
        db.commit()

    # 3. Audit Log (All -> Sector 4)
    audit = AuditLog(
        user_id=current_user.user_id,
        action="Case Update",
        resource="cases",
        resource_id=str(case.case_id)
    )
    db.add(audit)
    db.commit()
    
    return case

@router.post("/{case_id}/investigations", response_model=InvestigationNoteResponse, dependencies=[Depends(allow_officer)])
def add_investigation_note(case_id: int, note: InvestigationNoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not db.query(Case).filter(Case.case_id == case_id).first():
        raise HTTPException(status_code=404, detail="Case not found")
    new_note = InvestigationNote(
        case_id=case_id,
        officer_id=current_user.user_id,
        note_text=note.note_text
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.get("/{case_id}/activities", response_model=List[InvestigationActivityResponse], dependencies=[Depends(allow_officer)])
def get_investigation_activities(case_id: int, db: Session = Depends(get_db)):
    if not db.query(Case).filter(Case.case_id == case_id).first():
        raise HTTPException(status_code=404, detail="Case not found")
    return db.query(InvestigationActivity).filter(InvestigationActivity.case_id == case_id).order_by(InvestigationActivity.activity_date.desc()).all()

@router.post("/{case_id}/activities", response_model=InvestigationActivityResponse, dependencies=[Depends(allow_officer)])
def add_investigation_activity(case_id: int, activity: InvestigationActivityCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not db.query(Case).filter(Case.case_id == case_id).first():
        raise HTTPException(status_code=404, detail="Case not found")
    new_activity = InvestigationActivity(case_id=case_id, officer_id=current_user.user_id, action=activity.action, result=activity.result)
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity

@router.get("/{case_id}/evidence", dependencies=[Depends(allow_officer)])
def get_case_evidence(case_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    case = db.query(Case).filter(Case.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    evidence = db.query(Evidence).filter(Evidence.complaint_id == case.complaint_id).all()
    
    # Audit log
    audit = AuditLog(
        user_id=current_user.user_id,
        action="View Evidence",
        resource="evidence",
        resource_id=f"case_{case_id}"
    )
    db.add(audit)
    db.commit()
    
    return [{"evidence_id": e.evidence_id, "file_name": e.file_name, "status": e.status} for e in evidence]

@router.post("/{case_id}/evidence/custody", response_model=CustodyEventResponse, dependencies=[Depends(allow_officer)])
def log_chain_of_custody(case_id: int, custody: CustodyEventCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_custody = ChainOfCustody(
        evidence_id=custody.evidence_id,
        case_id=case_id,
        user_id=current_user.user_id,
        action=custody.action,
        notes=custody.notes
    )
    db.add(new_custody)
    db.commit()
    db.refresh(new_custody)
    
    # Audit log
    audit = AuditLog(
        user_id=current_user.user_id,
        action="Chain of Custody Update",
        resource="chain_of_custody",
        resource_id=str(new_custody.custody_id)
    )
    db.add(audit)
    db.commit()
    
    return new_custody

@router.post("/suspects", response_model=SuspectResponse, dependencies=[Depends(allow_officer)])
def add_suspect(suspect: SuspectCreate, db: Session = Depends(get_db)):
    new_suspect = Suspect(
        name_alias=suspect.name_alias,
        contact_info=suspect.contact_info,
        status=suspect.status,
        notes=suspect.notes
    )
    db.add(new_suspect)
    db.commit()
    db.refresh(new_suspect)
    return new_suspect

@router.post("/{case_id}/coordination", response_model=AgencyCoordinationResponse, dependencies=[Depends(allow_officer)])
def log_coordination(case_id: int, coord: AgencyCoordinationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_coord = AgencyCoordination(
        case_id=case_id,
        officer_id=current_user.user_id,
        organization_name=coord.organization_name,
        request_type=coord.request_type
    )
    db.add(new_coord)
    db.commit()
    db.refresh(new_coord)
    return new_coord
