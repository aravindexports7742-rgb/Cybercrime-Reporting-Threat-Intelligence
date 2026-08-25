from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class ComplaintCategoryBase(BaseModel):
    category_name: str
    description: Optional[str] = None

class ComplaintCategoryResponse(ComplaintCategoryBase):
    category_id: int
    class Config:
        from_attributes = True

class ComplaintCreate(BaseModel):
    category_id: int
    title: str
    incident_date: Optional[date] = None
    description: Optional[str] = None
    financial_loss: Optional[float] = 0.00
    suspected_url: Optional[str] = None
    suspected_phone: Optional[str] = None
    suspected_email: Optional[str] = None

class ComplaintResponse(ComplaintCreate):
    complaint_id: int
    tracking_id: str
    victim_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class EvidenceResponse(BaseModel):
    evidence_id: int
    file_name: str
    evidence_type: Optional[str]
    upload_date: datetime
    status: str
    class Config:
        from_attributes = True

class NotificationResponse(BaseModel):
    notification_id: int
    message: str
    event_type: Optional[str]
    is_read: bool
    created_at: datetime
    class Config:
        from_attributes = True
