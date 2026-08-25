from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class IncidentBase(BaseModel):
    incident_reference: str
    case_id: Optional[int] = None
    ioc_id: Optional[int] = None
    responder_id: Optional[int] = None
    incident_type: str
    description: Optional[str] = None
    severity: str = 'Low'
    status: str = 'Detected'

class IncidentCreate(IncidentBase):
    pass

class IncidentOut(IncidentBase):
    incident_id: int
    detected_at: datetime

    class Config:
        from_attributes = True

class IncidentUpdate(BaseModel):
    responder_id: Optional[int] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None

class IncidentActivityBase(BaseModel):
    action: str

class IncidentActivityCreate(IncidentActivityBase):
    pass

class IncidentActivityOut(IncidentActivityBase):
    activity_id: int
    incident_id: int
    performed_by: Optional[int]
    activity_time: datetime

    class Config:
        from_attributes = True

class ResponseActionBase(BaseModel):
    action_type: str
    description: Optional[str] = None

class ResponseActionCreate(ResponseActionBase):
    pass

class ResponseActionOut(ResponseActionBase):
    action_id: int
    incident_id: int
    performed_by: Optional[int]
    performed_at: datetime

    class Config:
        from_attributes = True

class PlaybookStepBase(BaseModel):
    step_order: int
    step_description: str

class PlaybookStepCreate(PlaybookStepBase):
    pass

class PlaybookStepOut(PlaybookStepBase):
    step_id: int
    playbook_id: int

    class Config:
        from_attributes = True

class PlaybookBase(BaseModel):
    playbook_name: str
    incident_type: Optional[str] = None
    description: Optional[str] = None

class PlaybookCreate(PlaybookBase):
    steps: Optional[List[PlaybookStepCreate]] = []

class PlaybookOut(PlaybookBase):
    playbook_id: int
    steps: List[PlaybookStepOut] = []

    class Config:
        from_attributes = True

class AuditLogOut(BaseModel):
    log_id: int
    user_id: Optional[int]
    action: str
    resource: Optional[str]
    resource_id: Optional[str]
    event_time: datetime
    ip_address: Optional[str]
    result: str

    class Config:
        from_attributes = True

class LoginHistoryOut(BaseModel):
    login_id: int
    user_id: Optional[int]
    event_type: str
    event_time: datetime
    ip_address: Optional[str]

    class Config:
        from_attributes = True

class SystemHealthOut(BaseModel):
    health_id: int
    component_name: str
    status: str
    checked_at: datetime
    details: Optional[str]

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    full_name: str
    email: str
    phone_number: Optional[str] = None
    password: str
    role_name: str

class UserUpdateRole(BaseModel):
    role_name: str

class UserOut(BaseModel):
    user_id: int
    full_name: str
    email: str
    phone_number: Optional[str]
    account_status: str
    created_at: datetime

    class Config:
        from_attributes = True

class RoleOut(BaseModel):
    role_id: int
    role_name: str
    description: Optional[str]

    class Config:
        from_attributes = True
