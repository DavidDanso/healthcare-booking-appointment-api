from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional

##########################################################👤 USER SCHEMAS
# 👤User schemas for input and validation

# 👤Represents the basic attributes required for a user (used for input validation)
class UserBase(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: str

# 👤Represents the attributes required for creating a new user
class UserCreate(UserBase):
    pass

# 👤Represents the attributes that can be updated for a user
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None

# 👤Represents the response data for a user
class UserResponseData(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        orm_mode = True  # 👤Enables SQLAlchemy ORM mode for this schema


################################################✅ LOGIN SCHEMAS
# ✅Schema for user login

# ✅Represents the attributes required for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


##########################################################🗿 PATIENT SCHEMAS
# 🗿Schemas for patient data

# 🗿Represents the basic attributes required for a patient (used for input validation)
class PatientBase(BaseModel):
    name: str
    dob: str
    gender: str
    phone: str

# 🗿Represents the attributes required for creating a new patient
class PatientCreate(PatientBase):
    pass

# 🗿Represents the attributes that can be updated for a patient
class PatientUpdate(BaseModel):
    name: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None

# 🗿Represents the response data for a patient
class PatientResponseData(BaseModel):
    id: int
    name: str
    dob: str
    gender: str
    phone: str
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


##########################################################🥼 DOCTOR SCHEMAS
# 🥼Schemas for doctor data

# 🥼Represents the basic attributes required for a doctor (used for input validation)
class DoctorBase(BaseModel):
    name: str
    specialty: str

# 🥼Represents the attributes required for creating a new doctor
class DoctorCreate(DoctorBase):
    pass

# 🥼Represents the attributes that can be updated for a doctor
class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialty: Optional[str] = None

# 🥼Represents the response data for a doctor
class DoctorResponseData(DoctorBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


##########################################################🏨 CLINIC SCHEMAS
# 🏨Schemas for clinic data

# 🏨Represents the basic attributes required for a clinic (used for input validation)
class ClinicBase(BaseModel):
    name: str
    address: str
    phone: str

# 🏨Represents the attributes required for creating a new clinic
class ClinicCreate(ClinicBase):
    pass

# 🏨Represents the attributes that can be updated for a clinic
class ClinicUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

# 🏨Represents the response data for a clinic
class ClinicResponseData(BaseModel):
    id: int
    name: str
    address: str
    phone: str
    created_at: datetime

    class Config:
        orm_mode = True


################################################################################################
# START OCTOR SCHEDULE DATA RSPONSE SCHEMAS🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼
################################################################################################
# 🥼Represents the response data for a doctor
class ScheduleDoctorResponseData(BaseModel):
    id: int
    name: str
    specialty: str

    class Config:
        orm_mode = True

# 🏨Represents the response data for a clinic
class ScheduleClinicResponseData(BaseModel):
    id: int
    name: str
    address: str
    phone: str

    class Config:
        orm_mode = True
################################################################################################
# END DOCTOR SCHEDULE DATA RSPONSE SCHEMAS🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼🥼
################################################################################################


##########################################################📌🥼 DOCTOR_SCHEDULE SCHEMAS
# 📌🥼Schemas for doctor schedule data

# 📌🥼Represents the basic attributes required for a doctor's schedule (used for input validation)
class DoctorScheduleBase(BaseModel):
    doctor_id: int
    clinic_id: int
    date: str
    slots: List[str]

# 📌🥼Represents the attributes required for creating a new doctor's schedule
class DoctorScheduleCreate(DoctorScheduleBase):
    pass

# 📌🥼Represents the attributes that can be updated for a doctor's schedule
class DoctorScheduleUpdate(BaseModel):
    doctor_id: Optional[int] = None
    clinic_id: Optional[int] = None
    date: Optional[str] = None
    slots: Optional[List[str]] = None

# 📌🥼Represents the response data for a doctor's schedule
class DoctorScheduleResponseData(BaseModel):
    schedule_id: int
    doctor: ScheduleDoctorResponseData
    clinic: ScheduleClinicResponseData
    date: str
    slots: List[str]

    class Config:
        orm_mode = True



################################################################################################
# START APPOINTMENT DATA RSPONSE SCHEMAS🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼
################################################################################################
# 🗿Represents the response data for a patient
class AppointmentPatientResponseData(BaseModel):
    name: str
    dob: str
    gender: str
    phone: str

    class Config:
        orm_mode = True

# 🥼Represents the response data for a doctor
class AppointmentDoctorResponseData(BaseModel):
    name: str
    specialty: str

    class Config:
        orm_mode = True

# 🏨Represents the response data for a clinic
class AppointmentClinicResponseData(BaseModel):
    name: str
    address: str
    phone: str

    class Config:
        orm_mode = True
################################################################################################
# END APPOINTMENT DATA RSPONSE SCHEMAS🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼🧑🏾‍💼👩🏾‍💼
################################################################################################



##########################################################🎟️ APPOINTMENT SCHEMAS
# 🎟️Schemas for patient appointment data

# 🎟️Represents the basic attributes required for a patient appointment (used for input validation)
class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    clinic_id: int
    appointment_date: str
    appointment_time: str

# 🎟️Represents the attributes required for creating a new patient's appointment
class AppointmentCreate(AppointmentBase):
    pass

# 🎟️Represents the attributes that can be updated for a patient's appointment
class AppointmentUpdate(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    clinic_id: Optional[int] = None
    appointment_date: Optional[str] = None
    appointment_time: Optional[str] = None

# 🎟️Represents the response data for a patient's appointment
class AppointmentResponseData(BaseModel):
    appointments_id: int
    patient: AppointmentPatientResponseData
    doctor: AppointmentDoctorResponseData
    clinic: AppointmentClinicResponseData
    appointment_date: str
    appointment_time: str
    appointment_status: str
    created_at: datetime

    class Config:
        orm_mode = True


################################📜 TOKEN SCHEMAS
# 📜Schemas for authentication tokens

# 📜Represents an authentication token
class Token(BaseModel):
    access_token: str
    token_type: str

# 📜Represents token data for a user
class TokenData(BaseModel):
    username: str | None = None

