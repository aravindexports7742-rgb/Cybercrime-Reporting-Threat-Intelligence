from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CaseResponse(BaseModel):
    case_id: int
    case_reference: str
    complaint_id: int
    lead_officer_id: Optional[int]
    priority: str
    status: str
    opened_at: datetime
    closed_at: Optional[datetime]
    class Config:
        from_attributes = True

class CaseUpdate(BaseModel):
    priority: Optional[str] = None
    status: Optional[str] = None

class InvestigationNoteCreate(BaseModel):
    note_text: str

class InvestigationNoteResponse(InvestigationNoteCreate):
    note_id: int
    case_id: int
    officer_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class SuspectCreate(BaseModel):
    name_alias: Optional[str] = None
    contact_info: Optional[str] = None
    status: Optional[str] = 'Person of Interest'
    notes: Optional[str] = None

class SuspectResponse(SuspectCreate):
    suspect_id: int
    class Config:
        from_attributes = True

class CustodyEventCreate(BaseModel):
    evidence_id: int
    action: str
    notes: Optional[str] = None

class CustodyEventResponse(CustodyEventCreate):
    custody_id: int
    case_id: int
    user_id: int
    event_time: datetime
    class Config:
        from_attributes = True

class AgencyCoordinationCreate(BaseModel):
    organization_name: str
    request_type: Optional[str] = None

class AgencyCoordinationResponse(AgencyCoordinationCreate):
    coordination_id: int
    case_id: int
    officer_id: int
    request_date: datetime
    status: str
    response: Optional[str]
    class Config:
        from_attributes = True
