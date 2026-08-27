from sqlalchemy import Column, Integer, String, Date, Text, Numeric, Enum, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from backend.database.connection import Base
from backend.models.shared_models import User
import datetime

class VictimProfile(Base):
    __tablename__ = "victim_profiles"
    victim_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE", onupdate="CASCADE"), unique=True, nullable=False)
    address = Column(String(255))
    date_of_birth = Column(Date)
    id_document_reference = Column(String(100))

    user = relationship("User")
    complaints = relationship("Complaint", back_populates="victim_profile")

class ComplaintCategory(Base):
    __tablename__ = "complaint_categories"
    category_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))

class Complaint(Base):
    __tablename__ = "complaints"
    complaint_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tracking_id = Column(String(20), unique=True, index=True, nullable=False)
    victim_id = Column(Integer, ForeignKey("victim_profiles.victim_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("complaint_categories.category_id", onupdate="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    incident_date = Column(Date)
    description = Column(Text)
    financial_loss = Column(Numeric(12, 2), default=0.00)
    suspected_url = Column(String(255))
    suspected_phone = Column(String(20))
    suspected_email = Column(String(150))
    status = Column(Enum('Submitted', 'Under Review', 'Assigned', 'Investigation', 'Action Taken', 'Resolved', 'Closed'), default='Submitted', nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)

    victim_profile = relationship("VictimProfile", back_populates="complaints")
    category = relationship("ComplaintCategory")
    evidence_list = relationship("Evidence", back_populates="complaint")
    notifications = relationship("Notification", back_populates="complaint")

class Evidence(Base):
    __tablename__ = "evidence"
    evidence_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    complaint_id = Column(Integer, ForeignKey("complaints.complaint_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.user_id", onupdate="CASCADE"), nullable=False)
    file_name = Column(String(255), nullable=False)
    evidence_type = Column(String(50))
    file_hash = Column(String(128))
    upload_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    status = Column(Enum('Active', 'Under Review', 'Archived'), default='Active', nullable=False)

    complaint = relationship("Complaint", back_populates="evidence_list")
    uploader = relationship("User")

class Notification(Base):
    __tablename__ = "notifications"
    notification_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    complaint_id = Column(Integer, ForeignKey("complaints.complaint_id", ondelete="CASCADE", onupdate="CASCADE"))
    message = Column(String(255), nullable=False)
    event_type = Column(String(50))
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    user = relationship("User")
    complaint = relationship("Complaint", back_populates="notifications")
