from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import datetime

from backend.database.connection import get_db
from backend.models.shared_models import User
from backend.models.sector1_victim import Complaint, Evidence, Notification, VictimProfile, ComplaintCategory
from backend.schemas.sector1_victim import ComplaintCreate, ComplaintResponse, EvidenceResponse, NotificationResponse
from backend.models.sector4_admin import AuditLog
from backend.models.sector2_officer import Case
from backend.security.auth import get_current_user
from backend.security.rbac import get_role_checker

router = APIRouter(prefix="/complaints", tags=["Sector 1: Victim Portal"])

allow_victim = get_role_checker(["Victim", "Administrator"])
allow_officer_admin = get_role_checker(["Officer", "Administrator", "Incident Responder"])

def get_victim_profile(user: User, db: Session):
    profile = db.query(VictimProfile).filter(VictimProfile.user_id == user.user_id).first()
    if not profile:
        profile = VictimProfile(user_id=user.user_id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.post("/", response_model=ComplaintResponse, dependencies=[Depends(allow_victim)])
def submit_complaint(complaint: ComplaintCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = get_victim_profile(current_user, db)
    
    # Generate tracking ID (simplified logic)
    current_year = datetime.datetime.now().year
    count = db.query(Complaint).count() + 1
    tracking_id = f"CYB-{current_year}-{count:06d}"
    
    new_complaint = Complaint(
        tracking_id=tracking_id,
        victim_id=profile.victim_id,
        category_id=complaint.category_id,
        title=complaint.title,
        incident_date=complaint.incident_date,
        description=complaint.description,
        financial_loss=complaint.financial_loss,
        suspected_url=complaint.suspected_url,
        suspected_phone=complaint.suspected_phone,
        suspected_email=complaint.suspected_email
    )
    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)
    
    # Auto-create a Case in Sector 2 so Officers can see it immediately
    case_count = db.query(Case).count() + 1
    case_reference = f"CASE-{datetime.datetime.now().year}-{case_count:06d}"
    new_case = Case(
        case_reference=case_reference,
        complaint_id=new_complaint.complaint_id,
        priority="Medium",
        status="New"
    )
    db.add(new_case)
    db.commit()

    # Audit log
    audit = AuditLog(
        user_id=current_user.user_id,
        action="Complaint Submission",
        resource="complaints",
        resource_id=new_complaint.tracking_id
    )
    db.add(audit)
    db.commit()
    
    return new_complaint

@router.get("/", response_model=List[ComplaintResponse], dependencies=[Depends(allow_victim)])
def get_complaints(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = get_victim_profile(current_user, db)
    return db.query(Complaint).filter(Complaint.victim_id == profile.victim_id).all()

# NOTE: This MUST be defined before /{case_id} to avoid FastAPI matching "notifications" as an int
@router.get("/notifications/list", response_model=List[NotificationResponse], dependencies=[Depends(allow_victim)])
def get_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Notification).filter(Notification.user_id == current_user.user_id).all()

@router.get("/categories", dependencies=[Depends(allow_victim)])
def get_categories(db: Session = Depends(get_db)):
    cats = db.query(ComplaintCategory).all()
    return [{"category_id": c.category_id, "category_name": c.category_name} for c in cats]

# Admin/Officer endpoint: returns ALL complaints across all victims (no victim_id filter)
# NOTE: Must be defined before /{case_id} to avoid route conflict
@router.get("/all", response_model=List[ComplaintResponse], dependencies=[Depends(allow_officer_admin)])
def get_all_complaints(db: Session = Depends(get_db)):
    """Returns every complaint in the system. Only accessible by Officers, Incident Responders, and Administrators."""
    return db.query(Complaint).order_by(Complaint.created_at.desc()).all()

@router.get("/{case_id}", response_model=ComplaintResponse, dependencies=[Depends(allow_victim)])
def get_complaint(case_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = get_victim_profile(current_user, db)
    complaint = db.query(Complaint).filter(Complaint.complaint_id == case_id, Complaint.victim_id == profile.victim_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint

@router.post("/{case_id}/evidence", response_model=EvidenceResponse, dependencies=[Depends(allow_victim)])
def upload_evidence(case_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = get_victim_profile(current_user, db)
    complaint = db.query(Complaint).filter(Complaint.complaint_id == case_id, Complaint.victim_id == profile.victim_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    new_evidence = Evidence(
        complaint_id=complaint.complaint_id,
        uploaded_by=current_user.user_id,
        file_name=file.filename,
        evidence_type=file.content_type
    )
    db.add(new_evidence)
    db.commit()
    db.refresh(new_evidence)
    
    # Audit log
    audit = AuditLog(
        user_id=current_user.user_id,
        action="Evidence Upload",
        resource="evidence",
        resource_id=str(new_evidence.evidence_id)
    )
    db.add(audit)
    db.commit()
    
    return new_evidence
