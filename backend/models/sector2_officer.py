from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.connection import Base
import datetime

class Case(Base):
    __tablename__ = "cases"
    case_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    case_reference = Column(String(30), unique=True, index=True, nullable=False)
    complaint_id = Column(Integer, ForeignKey("complaints.complaint_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    lead_officer_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL", onupdate="CASCADE"))
    priority = Column(Enum('Low', 'Medium', 'High', 'Critical'), default='Medium', nullable=False)
    status = Column(Enum('New', 'Under Review', 'Assigned', 'Investigation', 'Pending External Response', 'Action Taken', 'Resolved', 'Closed'), default='New', nullable=False)
    opened_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    closed_at = Column(DateTime, nullable=True)

    complaint = relationship("Complaint")
    lead_officer = relationship("User")
    assignments = relationship("CaseAssignment", back_populates="case")
    notes = relationship("InvestigationNote", back_populates="case")
    activities = relationship("InvestigationActivity", back_populates="case")

class CaseAssignment(Base):
    __tablename__ = "case_assignments"
    assignment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey("cases.case_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    officer_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    assigned_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL", onupdate="CASCADE"))
    assigned_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    unassigned_at = Column(DateTime, nullable=True)

    case = relationship("Case", back_populates="assignments")
    officer = relationship("User", foreign_keys=[officer_id])
    assigner = relationship("User", foreign_keys=[assigned_by])

class InvestigationNote(Base):
    __tablename__ = "investigation_notes"
    note_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey("cases.case_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    officer_id = Column(Integer, ForeignKey("users.user_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    note_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    case = relationship("Case", back_populates="notes")
    officer = relationship("User")

class InvestigationActivity(Base):
    __tablename__ = "investigation_activities"
    activity_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey("cases.case_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    officer_id = Column(Integer, ForeignKey("users.user_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    action = Column(String(255), nullable=False)
    result = Column(String(255))
    activity_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    case = relationship("Case", back_populates="activities")
    officer = relationship("User")

class Suspect(Base):
    __tablename__ = "suspects"
    suspect_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name_alias = Column(String(150))
    contact_info = Column(String(255))
    status = Column(Enum('Person of Interest', 'Confirmed', 'Cleared'), default='Person of Interest', nullable=False)
    notes = Column(Text)

class CaseSuspect(Base):
    __tablename__ = "case_suspects"
    case_id = Column(Integer, ForeignKey("cases.case_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    suspect_id = Column(Integer, ForeignKey("suspects.suspect_id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

class ChainOfCustody(Base):
    __tablename__ = "chain_of_custody"
    custody_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    evidence_id = Column(Integer, ForeignKey("evidence.evidence_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    case_id = Column(Integer, ForeignKey("cases.case_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    action = Column(String(100), nullable=False)
    event_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    notes = Column(String(255))

    evidence = relationship("Evidence")
    case = relationship("Case")
    user = relationship("User")

class EvidenceAccessHistory(Base):
    __tablename__ = "evidence_access_history"
    access_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    evidence_id = Column(Integer, ForeignKey("evidence.evidence_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    access_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    access_type = Column(Enum('View', 'Download', 'Analyze'), default='View', nullable=False)

class AgencyCoordination(Base):
    __tablename__ = "agency_coordination"
    coordination_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey("cases.case_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    officer_id = Column(Integer, ForeignKey("users.user_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    organization_name = Column(String(150), nullable=False)
    request_type = Column(String(100))
    request_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    status = Column(Enum('Pending', 'Responded', 'Closed'), default='Pending', nullable=False)
    response = Column(Text)

    case = relationship("Case")
    officer = relationship("User")
