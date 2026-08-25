from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.connection import Base
import datetime


class ThreatSource(Base):
    __tablename__ = "threat_sources"
    source_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    source_name = Column(String(150), nullable=False)
    source_type = Column(String(100))
    reliability_rating = Column(Enum('Low', 'Medium', 'High'), default='Medium')

    feeds = relationship("ThreatFeed", back_populates="source")


class ThreatFeed(Base):
    __tablename__ = "threat_feeds"
    feed_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    source_id = Column(Integer, ForeignKey("threat_sources.source_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    ingested_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    record_count = Column(Integer, default=0)
    status = Column(Enum('Success', 'Partial', 'Failed'), default='Success', nullable=False)

    source = relationship("ThreatSource", back_populates="feeds")


class ThreatCategory(Base):
    __tablename__ = "threat_categories"
    category_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))


class IOC(Base):
    __tablename__ = "iocs"
    ioc_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ioc_type = Column(Enum('IP', 'Domain', 'URL', 'Hash', 'Email'), nullable=False)
    ioc_value = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey("threat_categories.category_id", ondelete="SET NULL", onupdate="CASCADE"))
    source_id = Column(Integer, ForeignKey("threat_sources.source_id", ondelete="SET NULL", onupdate="CASCADE"))
    risk_level = Column(Enum('Low', 'Medium', 'High', 'Critical'), default='Low', nullable=False)
    first_seen = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    last_seen = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    category = relationship("ThreatCategory")
    source = relationship("ThreatSource")
    malware_indicators = relationship("MalwareIndicator", back_populates="ioc")


class MalwareIndicator(Base):
    __tablename__ = "malware_indicators"
    malware_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ioc_id = Column(Integer, ForeignKey("iocs.ioc_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    malware_family = Column(String(150))
    signature = Column(String(255))
    description = Column(Text)

    ioc = relationship("IOC", back_populates="malware_indicators")


class Campaign(Base):
    __tablename__ = "campaigns"
    campaign_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    campaign_name = Column(String(150), nullable=False)
    description = Column(Text)
    risk_level = Column(Enum('Low', 'Medium', 'High', 'Critical'), default='Medium', nullable=False)
    detected_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)


class CampaignIOC(Base):
    __tablename__ = "campaign_iocs"
    campaign_id = Column(Integer, ForeignKey("campaigns.campaign_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    ioc_id = Column(Integer, ForeignKey("iocs.ioc_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)


class ComplaintIOC(Base):
    __tablename__ = "complaint_iocs"
    complaint_id = Column(Integer, ForeignKey("complaints.complaint_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    ioc_id = Column(Integer, ForeignKey("iocs.ioc_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)


class ThreatRelationship(Base):
    __tablename__ = "threat_relationships"
    relationship_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ioc_id_a = Column(Integer, ForeignKey("iocs.ioc_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    ioc_id_b = Column(Integer, ForeignKey("iocs.ioc_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    relationship_type = Column(String(100))
    confidence_level = Column(Enum('Low', 'Medium', 'High'), default='Medium', nullable=False)

    ioc_a = relationship("IOC", foreign_keys=[ioc_id_a])
    ioc_b = relationship("IOC", foreign_keys=[ioc_id_b])


class ThreatAnalysisResult(Base):
    __tablename__ = "threat_analysis_results"
    result_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    related_case_id = Column(Integer, ForeignKey("cases.case_id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    analysis_type = Column(String(100))
    summary = Column(Text)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
