from typing import List
from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/schedules'
)

########################### ADD NEW DOCTOR SCHEDULE [ CREATE ] ###########################

# This route handles the addition of a new doctor's schedule. A JSON payload containing
# schedule details according to the DoctorScheduleCreate schema is expected. 
# Authentication through OAuth2 is enforced, and the user must have the 'admin' role.

@router.post("/", response_model=schemas.DoctorScheduleResponseData, status_code=status.HTTP_201_CREATED)
def add_schedule(schedule_data: schemas.DoctorScheduleCreate, db: Session = Depends(get_db), 
                 current_user: dict = Depends(oauth2.get_current_user)):
    
    # Get doctor and clinic based on IDs from the payload.
    doctor = db.query(models.Doctor).filter(models.Doctor.id == schedule_data.doctor_id).first()
    clinic = db.query(models.Clinic).filter(models.Clinic.id == schedule_data.clinic_id).first()

    # Check if the authenticated user has the 'admin' role.
    isAdmin = current_user.role == 'admin'

    if isAdmin:
        # Create a new DoctorSchedule object from the provided schedule data.
        new_schedule = models.DoctorSchedule(
            doctor_fkey=schedule_data.doctor_id,
            clinic_fkey=schedule_data.clinic_id,
            **schedule_data.dict()
        )

        # Check if doctor or clinic is not found in the database.
        if doctor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Doctor with ID: {schedule_data.doctor_id}, not found!"
            )

        if clinic is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Clinic with ID: {schedule_data.clinic_id}, not found!"
            )

        # Fetch existing doctors and schedules from the database.
        get_doctors = db.query(models.Doctor).all()
        get_schedule = db.query(models.DoctorSchedule).all()

        # Extract doctor IDs and existing schedule slots.
        doctors_arr = [doc.id for doc in get_doctors]
        schedule_arr = [sch.slots for sch in get_schedule]

        # Check if doctor_id is already in the database and if the time slot is already booked.
        if schedule_data.doctor_id in doctors_arr and schedule_data.slots in schedule_arr:
            # Raise a Forbidden error if the doctor is already booked.
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"{doctor.name} has already been scheduled for this timeframe."
            )

        # Add the new schedule to the database.
        db.add(new_schedule)

        # Commit the changes to the database.
        db.commit()

        # Refresh the object to ensure it reflects the latest state from the database.
        db.refresh(new_schedule)

        # Return the newly created schedule as a response.
        return new_schedule
    else:
        # If the user is not an admin, raise a 403 Forbidden error.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can add doctor schedules."
        )

    

########################### GET ALL DOCTORS SCHEDULES [ READ ] ###########################

# This route allows retrieving all doctor schedules. It returns a list of doctor schedules
# in the response. No authentication is required for this route.
@router.get("/", response_model=List[schemas.DoctorScheduleResponseData])
def get_schedules(db: Session = Depends(get_db)):
    # Query the database to retrieve all doctor schedules.
    all_schedules = db.query(models.DoctorSchedule).all()

    # Return the list of schedules as a response.
    return all_schedules



