from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# --- Threat Sources ---
class ThreatSourceCreate(BaseModel):
    source_name: str
    source_type: Optional[str] = None
    reliability_rating: Optional[str] = 'Medium'

class ThreatSourceResponse(ThreatSourceCreate):
    source_id: int
    class Config:
        from_attributes = True


# --- Threat Feeds ---
class ThreatFeedCreate(BaseModel):
    source_id: int
    record_count: Optional[int] = 0
    status: Optional[str] = 'Success'

class ThreatFeedResponse(ThreatFeedCreate):
    feed_id: int
    ingested_at: datetime
    class Config:
        from_attributes = True


# --- IOCs ---
class IOCCreate(BaseModel):
    ioc_type: str  # IP, Domain, URL, Hash, Email
    ioc_value: str
    category_id: Optional[int] = None
    source_id: Optional[int] = None
    risk_level: Optional[str] = 'Low'

class IOCResponse(IOCCreate):
    ioc_id: int
    first_seen: datetime
    last_seen: datetime
    class Config:
        from_attributes = True


# --- Campaigns ---
class CampaignCreate(BaseModel):
    campaign_name: str
    description: Optional[str] = None
    risk_level: Optional[str] = 'Medium'

class CampaignResponse(CampaignCreate):
    campaign_id: int
    detected_at: datetime
    class Config:
        from_attributes = True


# --- Threat Analysis Results ---
class ThreatAnalysisResultResponse(BaseModel):
    result_id: int
    related_case_id: Optional[int]
    analysis_type: Optional[str]
    summary: Optional[str]
    generated_at: datetime
    class Config:
        from_attributes = True
