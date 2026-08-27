from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from backend.database.connection import Base
import datetime

class Incident(Base):
    __tablename__ = "incidents"
    incident_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    incident_reference = Column(String(30), unique=True, index=True, nullable=False)
    case_id = Column(Integer, ForeignKey("cases.case_id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    ioc_id = Column(Integer, ForeignKey("iocs.ioc_id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    responder_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    incident_type = Column(String(100), nullable=False)
    description = Column(Text)
    severity = Column(Enum('Low', 'Medium', 'High', 'Critical'), default='Low', nullable=False)
    status = Column(Enum('Detected', 'Triage', 'Investigating', 'Containing', 'Remediating', 'Recovering', 'Resolved', 'Closed'), default='Detected', nullable=False)
    detected_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    case = relationship("Case")
    ioc = relationship("IOC")
    responder = relationship("User")
    activities = relationship("IncidentActivity", back_populates="incident")
    response_actions = relationship("ResponseAction", back_populates="incident")


class IncidentActivity(Base):
    __tablename__ = "incident_activities"
    activity_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    incident_id = Column(Integer, ForeignKey("incidents.incident_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    performed_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    action = Column(String(255), nullable=False)
    activity_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    incident = relationship("Incident", back_populates="activities")
    user = relationship("User")


class ResponseAction(Base):
    __tablename__ = "response_actions"
    action_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    incident_id = Column(Integer, ForeignKey("incidents.incident_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    action_type = Column(String(100), nullable=False)
    description = Column(Text)
    performed_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    performed_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    incident = relationship("Incident", back_populates="response_actions")
    user = relationship("User")


class Playbook(Base):
    __tablename__ = "playbooks"
    playbook_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    playbook_name = Column(String(150), nullable=False)
    incident_type = Column(String(100))
    description = Column(Text)

    steps = relationship("PlaybookStep", back_populates="playbook")


class PlaybookStep(Base):
    __tablename__ = "playbook_steps"
    step_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    playbook_id = Column(Integer, ForeignKey("playbooks.playbook_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    step_order = Column(Integer, nullable=False)
    step_description = Column(String(255), nullable=False)

    playbook = relationship("Playbook", back_populates="steps")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    log_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    action = Column(String(150), nullable=False)
    resource = Column(String(100))
    resource_id = Column(String(50))
    event_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    ip_address = Column(String(45))
    result = Column(Enum('Success', 'Failure'), default='Success', nullable=False)

    user = relationship("User")


class LoginHistory(Base):
    __tablename__ = "login_history"
    login_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    event_type = Column(Enum('Login Success', 'Login Failed', 'Logout'), nullable=False)
    event_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    ip_address = Column(String(45))

    user = relationship("User")


class SystemHealth(Base):
    __tablename__ = "system_health"
    health_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    component_name = Column(String(100), nullable=False)
    status = Column(Enum('Healthy', 'Warning', 'Down'), default='Healthy', nullable=False)
    checked_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    details = Column(String(255))
