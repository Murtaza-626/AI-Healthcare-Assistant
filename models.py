"""
models.py
SQLAlchemy ORM models strictly matching the FYP ER Diagram specification.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Date, DateTime, Numeric, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    patients = relationship("Patient", back_populates="doctor", cascade="all, delete-orphan")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    doctor = relationship("Doctor", back_populates="patients")
    consultations = relationship("Consultation", back_populates="patient", cascade="all, delete-orphan")


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    symptoms = Column(JSONB, nullable=True)  # List/Dictionary of recorded symptoms
    urdu_audio_transcript = Column(Text, nullable=True)
    english_translation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    patient = relationship("Patient", back_populates="consultations")
    lab_reports = relationship("LabReport", back_populates="consultation", cascade="all, delete-orphan")
    prediction = relationship("Prediction", back_populates="consultation", uselist=False, cascade="all, delete-orphan")


class LabReport(Base):
    __tablename__ = "lab_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    consultation_id = Column(UUID(as_uuid=True), ForeignKey("consultations.id", ondelete="CASCADE"), nullable=False)
    report_image_url = Column(String(500), nullable=True)
    extracted_ocr_data = Column(JSONB, nullable=True)  # Data returned by Google Gemini OCR
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    consultation = relationship("Consultation", back_populates="lab_reports")


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    consultation_id = Column(UUID(as_uuid=True), ForeignKey("consultations.id", ondelete="CASCADE"), nullable=False, unique=True)
    predicted_disease = Column(String(255), nullable=False)
    risk_percentage = Column(Numeric(5, 2), nullable=False)
    llm_clinical_summary = Column(Text, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    consultation = relationship("Consultation", back_populates="prediction")