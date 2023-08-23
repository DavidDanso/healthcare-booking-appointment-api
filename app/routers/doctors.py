from typing import List
from fastapi import Depends, Response, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/doctors'
)

########################### ADD NEW DOCTOR [ CREATE ] ###########################

# Endpoint to add a new doctor. Requires an authenticated admin user.
@router.post("/", response_model=schemas.DoctorResponseData, status_code=status.HTTP_201_CREATED)
def add_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db), 
               current_user: dict = Depends(oauth2.get_current_user)):
    
    # Check if the current user is an admin.
    isAdmin = current_user.role == 'admin'

    if isAdmin:
        # Create a new Doctor instance from the incoming data.
        new_doctor = models.Doctor(**doctor.dict())
        all_doctors = db.query(models.Doctor).all()

        # Check if doctor's name is already in the database.
        if doctor.name in [doc.name for doc in all_doctors]:
            # Raise a Forbidden error if the doctor is already in the database.
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail=f"This Doctor is already in the database.")

        # Add the new doctor to the database.
        db.add(new_doctor)

        # Commit the transaction to persist the changes.
        db.commit()

        # Refresh the doctor object to ensure it reflects the database state.
        db.refresh(new_doctor)
        return new_doctor
    else:
        # Raise a Forbidden error if the user is not an admin.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Only admin can add new doctors.")


########################### GET ALL DOCTORS [ READ ] ###########################

# Endpoint to retrieve a list of all doctors.
@router.get("/", response_model=List[schemas.DoctorResponseData])
def get_doctors(db: Session = Depends(get_db)):

    # Query the database to retrieve all doctors.
    all_doctors = db.query(models.Doctor).all()

    return all_doctors


########################## GET DOCTOR WITH ID [ READ ] ###########################

# Endpoint to retrieve a specific doctor by ID.
@router.get("/{doctor_id}", response_model=schemas.DoctorResponseData)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):

    # Query the database to retrieve the doctor with the specified ID.
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()

    if not doctor:
        # Raise a Not Found error if the doctor is not found.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Doctor with ID: {doctor_id}, not found!")

    return doctor


########################### UPDATE DOCTOR [ UPDATE ] ###########################

# Endpoint to update a doctor's information by ID. Requires an authenticated admin user.
@router.put("/{doctor_id}", response_model=schemas.DoctorResponseData)
def update_doctor(doctor_id: int, doctor_update: schemas.DoctorUpdate, db: Session = Depends(get_db),
                  current_user: dict = Depends(oauth2.get_current_user)):

    # Query the database to find the doctor to be updated.
    doc_query = db.query(models.Doctor).filter(models.Doctor.id == doctor_id)

    if not doc_query.first():
        # Raise a Not Found error if the doctor is not found.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Doctor with ID: {doctor_id}, not found!")
    
    if current_user.role != 'admin':
        # Raise a Forbidden error if the user is not an admin.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Only admin can update a doctor")
    
    # Update the doctor's data in the database.
    doc_query.update(doctor_update.model_dump(exclude_unset=True), synchronize_session=False)

    # Commit the transaction to persist the changes.
    db.commit()

    # Refresh the doctor object to ensure it reflects the updated state.
    db.refresh(doc_query.first())

    return doc_query.first()


########################### DELETE DOCTOR [ DELETE ] ###########################

# Endpoint to delete a doctor by ID. Requires an authenticated admin user.
@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db), 
                  current_user: dict = Depends(oauth2.get_current_user)):

    # Query the database to find the doctor to be deleted.
    doc_query = db.query(models.Doctor).filter(models.Doctor.id == doctor_id)
    doctor = doc_query.first()

    if not doctor:
        # Raise a Not Found error if the doctor is not found.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Doctor with ID: {doctor_id}, not found!")
    
    if current_user.role != 'admin':
        # Raise a Forbidden error if the user is not an admin.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Only admin can delete a doctor")
    
    # Delete the doctor from the database.
    doc_query.delete(synchronize_session=False)

    # Commit the transaction to persist the changes.
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


########################################################################################
# READ, UPDATE & DELETE DOCTOR SCHEDULES 
########################################################################################

########################### GET ALL DOCTORS SCHEDULES WITH ID [ READ ] ###########################
####📌 work on the schedule. if doctor is not added return a 404 error 📌###
# Endpoint to retrieve all schedules for a specific doctor identified by 'doctor_id'
@router.get("/{doctor_id}/schedules", response_model=List[schemas.DoctorScheduleResponseData])
def get_doctor_schedules(doctor_id: int, db: Session = Depends(get_db)):
    # Query the database to retrieve all schedules for the specified doctor
    doctor_schedule = db.query(models.DoctorSchedule).filter(models.DoctorSchedule.doctor_id == doctor_id).all()

    # If no schedules are found, raise a 404 error
    if not doctor_schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Doctor with ID: {doctor_id}, not found!")

    # Return the retrieved doctor schedules
    return doctor_schedule


########################### UPDATE DOCTORS SCHEDULES WITH ID [ PUT ] ###########################

# Endpoint to update a specific doctor's schedule identified by 'id'
@router.put("/{schedule_id}/schedules", response_model=schemas.DoctorScheduleResponseData)
def update_doctor_schedules(schedule_id: int, schedule_update: schemas.DoctorScheduleUpdate, db: Session = Depends(get_db),
                         current_user: dict = Depends(oauth2.get_current_user)):
    # Query the database to retrieve the doctor schedule with the given 'id'
    schedules_query = db.query(models.DoctorSchedule).filter(models.DoctorSchedule.schedule_id == schedule_id)
    schedule = schedules_query.first()

    # If no schedule is found, raise a 404 error
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Doctor Schedule with ID: {schedule_id}, not found!")

    # Only admin users are allowed to update doctor schedules
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Only admin can update doctor schedule.")
    
    # Update the doctor schedule with the provided data
    schedules_query.update(schedule_update.model_dump(exclude_unset=True), synchronize_session=False)

    # Commit the changes to the database
    db.commit()

    # Refresh and retrieve the updated doctor schedule
    db.refresh(schedule)

    return schedule


########################### DELETE DOCTORS SCHEDULES WITH ID [ DELETE ] ###########################

# Endpoint to delete a specific doctor's schedule identified by 'id'
@router.delete("/{schedule_id}/schedules", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor_schedules(schedule_id: int, db: Session = Depends(get_db),
                         current_user: dict = Depends(oauth2.get_current_user)):
    # Query the database to retrieve the doctor schedule with the given 'id'
    schedule_query = db.query(models.DoctorSchedule).filter(models.DoctorSchedule.schedule_id == schedule_id)
    schedule = schedule_query.first()

    # If no schedule is found, raise a 404 error
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Doctor Schedule with ID: {schedule_id}, not found!")

    # Only admin users are allowed to delete doctor schedules
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Only admin can delete doctor schedule.")
    
    # Delete the doctor schedule from the database
    schedule_query.delete(synchronize_session=False)

    # Commit the changes to the database
    db.commit()

    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
