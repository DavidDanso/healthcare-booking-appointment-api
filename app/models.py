from sqlalchemy import ARRAY, TIMESTAMP, Column, ForeignKey, Integer, String, text
from .database import Base
from sqlalchemy.orm import relationship

# Class representing appointments information
class Appointment(Base):
    __tablename__ = "appointments"

    appointments_id = Column(Integer, primary_key=True, index=True, nullable=False)  # Unique identifier for the appointment
    patient_id = Column(Integer, nullable=False)
    doctor_id = Column(Integer, nullable=False)
    clinic_id = Column(Integer, nullable=False)
   
    user_fkey = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    patient_fkey = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    doctor_fkey = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    clinic_fkey = Column(Integer, ForeignKey("clinics.id", ondelete="CASCADE"), nullable=False)
    
    patient = relationship("Patient")
    doctor = relationship("Doctor")
    clinic = relationship("Clinic")

    appointment_date = Column(String, nullable=False) # appointment date format [ YY-MM-DD - hh:mm:ss ]
    appointment_time = Column(String, nullable=False) # appointment time format [ HH:MM AM/PM ]
    appointment_status = Column(String, nullable=False, default='booked')  # appointment status
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)  # Creation timestamp


# Class representing doctor availability schedule
class DoctorSchedule(Base):
    __tablename__ = 'schedules'

    schedule_id = Column(Integer, primary_key=True, index=True, nullable=False)  # Unique identifier for the schedule
    
    doctor_id = Column(Integer, nullable=False)  # ID of the associated doctor
    clinic_id = Column(Integer, nullable=False)  # ID of the associated clinic
    date = Column(String, nullable=False)  # Date of the availability schedule
    slots = Column(ARRAY(String), nullable=False)  # Time slots for appointments

    doctor_fkey = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    clinic_fkey = Column(Integer, ForeignKey("clinics.id", ondelete="CASCADE"), nullable=False)

    doctor = relationship("Doctor")
    clinic = relationship("Clinic")
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)  # Creation timestamp


# Class representing user information
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)  # Unique identifier for the user
    username = Column(String, unique=True, index=True, nullable=False)  # User's username
    password = Column(String, index=True, nullable=False)  # User's password (hashed)
    email = Column(String, unique=True, index=True, nullable=False)  # User's email address
    role = Column(String, index=True, nullable=False)  # Role of the user (e.g., patient, doctor, admin)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)  # Creation timestamp


# Class representing patient information
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True, nullable=False)  # Unique identifier for the patient
    name = Column(String, unique=True, index=True, nullable=False)  # Patient's name
    dob = Column(String, index=True, nullable=False)  # Date of birth
    gender = Column(String, index=True, nullable=False)  # Gender of the patient
    phone = Column(String, index=True, nullable=False)  # Contact phone number
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # Associated user ID
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)  # Creation timestamp


# Class representing doctor information
class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True, nullable=False)  # Unique identifier for the doctor
    name = Column(String, unique=True, index=True, nullable=False)  # Doctor's name
    specialty = Column(String, index=True, nullable=False)  # Medical specialty of the doctor
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)  # Creation timestamp


# Class representing clinic information
class Clinic(Base):
    __tablename__ = "clinics"

    id = Column(Integer, primary_key=True, index=True, nullable=False)  # Unique identifier for the clinic
    name = Column(String, unique=True, index=True, nullable=False)  # Clinic's name
    address = Column(String, nullable=False)  # Address of the clinic
    phone = Column(String, unique=True, nullable=False)  # Contact phone number for the clinic
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)  # Creation timestamp