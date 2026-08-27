from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from backend.database.connection import get_db
from backend.models.shared_models import User
from backend.models.sector3_threat import (
    ThreatSource, ThreatFeed, ThreatCategory, IOC, MalwareIndicator,
    Campaign, CampaignIOC, ComplaintIOC, ThreatRelationship, ThreatAnalysisResult
)
from backend.schemas.sector3_threat import (
    ThreatSourceCreate, ThreatSourceResponse,
    ThreatFeedCreate, ThreatFeedResponse,
    IOCCreate, IOCResponse,
    CampaignCreate, CampaignResponse,
    ThreatAnalysisResultResponse
)
from backend.models.sector4_admin import AuditLog, Incident
from backend.security.auth import get_current_user
from backend.security.rbac import get_role_checker
import datetime

router = APIRouter(tags=["Sector 3: Threat Intelligence"])

allow_analyst = get_role_checker(["Threat Analyst", "Administrator"])


# ===================== Threat Sources =====================

@router.post("/threat-feeds", response_model=ThreatFeedResponse, dependencies=[Depends(allow_analyst)])
def ingest_threat_feed(feed: ThreatFeedCreate, db: Session = Depends(get_db)):
    source = db.query(ThreatSource).filter(ThreatSource.source_id == feed.source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Threat source not found")
    new_feed = ThreatFeed(
        source_id=feed.source_id,
        record_count=feed.record_count,
        status=feed.status
    )
    db.add(new_feed)
    db.commit()
    db.refresh(new_feed)
    return new_feed


@router.get("/threat-feeds", response_model=List[ThreatFeedResponse], dependencies=[Depends(allow_analyst)])
def list_threat_feeds(db: Session = Depends(get_db)):
    return db.query(ThreatFeed).all()


# ===================== IOCs =====================

@router.post("/iocs", response_model=IOCResponse, dependencies=[Depends(allow_analyst)])
def register_ioc(ioc: IOCCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Duplicate check
    existing = db.query(IOC).filter(IOC.ioc_type == ioc.ioc_type, IOC.ioc_value == ioc.ioc_value).first()
    if existing:
        raise HTTPException(status_code=400, detail="IOC already exists")
    new_ioc = IOC(
        ioc_type=ioc.ioc_type,
        ioc_value=ioc.ioc_value,
        category_id=ioc.category_id,
        source_id=ioc.source_id,
        risk_level=ioc.risk_level
    )
    db.add(new_ioc)
    db.commit()
    db.refresh(new_ioc)
    
    # Audit log
    audit = AuditLog(
        user_id=current_user.user_id,
        action="Register IOC",
        resource="iocs",
        resource_id=str(new_ioc.ioc_id)
    )
    db.add(audit)
    db.commit()

    # Threat Escalation (Sector 3 -> Sector 4)
    if new_ioc.risk_level == "Critical":
        incident = Incident(
            incident_reference=f"INC-IOC-{new_ioc.ioc_id}-{int(datetime.datetime.now().timestamp())}",
            ioc_id=new_ioc.ioc_id,
            incident_type="Critical IOC Detected",
            description=f"Critical IOC registered: {new_ioc.ioc_value} of type {new_ioc.ioc_type}",
            severity="Critical",
            status="Detected"
        )
        db.add(incident)
        db.commit()
    
    return new_ioc


@router.get("/iocs", response_model=List[IOCResponse], dependencies=[Depends(allow_analyst)])
def list_iocs(db: Session = Depends(get_db)):
    return db.query(IOC).all()


# NOTE: /iocs/search MUST be defined BEFORE /iocs/{ioc_id} to prevent FastAPI
# from matching the literal string "search" as an integer ioc_id (which causes 422).
@router.get("/iocs/search", response_model=List[IOCResponse], dependencies=[Depends(allow_analyst)])
def search_iocs(value: str = Query(...), db: Session = Depends(get_db)):
    results = db.query(IOC).filter(IOC.ioc_value.contains(value)).all()
    return results


@router.get("/iocs/{ioc_id}", response_model=IOCResponse, dependencies=[Depends(allow_analyst)])
def get_ioc(ioc_id: int, db: Session = Depends(get_db)):
    ioc = db.query(IOC).filter(IOC.ioc_id == ioc_id).first()
    if not ioc:
        raise HTTPException(status_code=404, detail="IOC not found")
    return ioc


# ===================== Threats (IOC detail) =====================

@router.get("/threats", response_model=List[IOCResponse], dependencies=[Depends(allow_analyst)])
def list_threats(db: Session = Depends(get_db)):
    return db.query(IOC).filter(IOC.risk_level.in_(['High', 'Critical'])).all()


@router.get("/threats/{threat_id}", response_model=IOCResponse, dependencies=[Depends(allow_analyst)])
def get_threat(threat_id: int, db: Session = Depends(get_db)):
    ioc = db.query(IOC).filter(IOC.ioc_id == threat_id).first()
    if not ioc:
        raise HTTPException(status_code=404, detail="Threat not found")
    return ioc


# ===================== Campaigns =====================

@router.get("/campaigns", response_model=List[CampaignResponse], dependencies=[Depends(allow_analyst)])
def list_campaigns(db: Session = Depends(get_db)):
    return db.query(Campaign).all()


@router.get("/campaigns/{campaign_id}", response_model=CampaignResponse, dependencies=[Depends(allow_analyst)])
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.campaign_id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


# ===================== Trend & Forecast =====================

@router.get("/threat-trends", dependencies=[Depends(allow_analyst)])
def threat_trends(db: Session = Depends(get_db)):
    """Returns IOC counts grouped by type and risk level for trend analysis."""
    by_type = db.query(IOC.ioc_type, func.count(IOC.ioc_id)).group_by(IOC.ioc_type).all()
    by_risk = db.query(IOC.risk_level, func.count(IOC.ioc_id)).group_by(IOC.risk_level).all()
    return {
        "by_type": [{"ioc_type": t, "count": c} for t, c in by_type],
        "by_risk": [{"risk_level": r, "count": c} for r, c in by_risk],
    }


@router.get("/threat-forecast", dependencies=[Depends(allow_analyst)])
def threat_forecast(db: Session = Depends(get_db)):
    """Returns simple forecast data based on recent IOC ingestion rate."""
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    last_7 = now - timedelta(days=7)
    last_30 = now - timedelta(days=30)

    recent_7 = db.query(func.count(IOC.ioc_id)).filter(IOC.first_seen >= last_7).scalar() or 0
    recent_30 = db.query(func.count(IOC.ioc_id)).filter(IOC.first_seen >= last_30).scalar() or 0
    total = db.query(func.count(IOC.ioc_id)).scalar() or 0

    return {
        "total_iocs": total,
        "last_7_days": recent_7,
        "last_30_days": recent_30,
        "avg_daily_7d": round(recent_7 / 7, 2) if recent_7 else 0,
        "avg_daily_30d": round(recent_30 / 30, 2) if recent_30 else 0,
    }
