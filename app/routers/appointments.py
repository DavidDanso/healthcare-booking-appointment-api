from typing import List
from fastapi import Depends, Response, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/appointments'
)

"""
    Endpoint to create a new appointment.
    
    Args:
        appointment_data (schemas.AppointmentCreate): Data for the new appointment.
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (dict, optional): Currently logged-in user. Defaults to Depends(oauth2.get_current_user).
    
    Returns:
        schemas.AppointmentResponseData: Created appointment data.
"""
########################### ADD NEW APPOINTMENT [ CREATE ] ###########################
@router.post("/", response_model=schemas.AppointmentResponseData, status_code=status.HTTP_201_CREATED)
def add_appointment(appointment_data: schemas.AppointmentCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    # Fetch patient, doctor, clinic, and schedule records
    patient = db.query(models.Patient).get(appointment_data.patient_id)
    doctor = db.query(models.Doctor).get(appointment_data.doctor_id)
    clinic = db.query(models.Clinic).get(appointment_data.clinic_id)
    doc_schedule = db.query(models.DoctorSchedule).filter_by(doctor_id=appointment_data.doctor_id).first()
    
    # Fetch all existing appointments
    all_appointments = db.query(models.Appointment).all()
    doctors_ids_arr = [appointment.doctor_id for appointment in all_appointments]
    appointment_date_time_set = {(appointment.appointment_date, appointment.appointment_time) for appointment in all_appointments}
    

    # Check if doctor is already booked
    is_doctor_booked = (appointment_data.doctor_id in doctors_ids_arr) and \
                       ((appointment_data.appointment_date, appointment_data.appointment_time) in appointment_date_time_set)

    # Create a new appointment instance
    new_appointment = models.Appointment(
        patient_fkey=appointment_data.patient_id,
        doctor_fkey=appointment_data.doctor_id,
        clinic_fkey=appointment_data.clinic_id,
        user_fkey=current_user.id,
        **appointment_data.dict()
    )
    
    # Handle cases where patient, doctor, clinic, or schedule is not found
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with ID: {appointment_data.patient_id} not found")
    
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Doctor with ID: {appointment_data.doctor_id} not found")
    
    if not clinic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Clinic with ID: {appointment_data.clinic_id} not found")
    
    if not doc_schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking for {doctor.name} is currently unavailable")
    

    # Check if the doctor is already booked for the chosen date and time
    if is_doctor_booked:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{doctor.name} is already booked for this timeframe")
    

    # Check if the chosen appointment date is within the doctor's schedule date
    if appointment_data.appointment_date != doc_schedule.date:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{doctor.name} does not have a schedule for this date: {doc_schedule.date}."
        )
    
    # Check if the chosen appointment time is within the doctor's available time slots
    if appointment_data.appointment_time not in doc_schedule.slots:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{doctor.name} has time schedules for these times: {doc_schedule.slots}."
        )
    
    # Check if the chosen clinic is the same as the one where the doctor has a schedule
    if appointment_data.clinic_id != doc_schedule.clinic_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{doctor.name} does not have a schedule at {clinic.name}."
        )


    # Add the new appointment to the database
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


    
########################### GET ALL APPOINTMENTS [ READ ] ###########################
@router.get("/", response_model=List[schemas.AppointmentResponseData])
def get_appointments(db: Session = Depends(get_db), 
                     current_user: dict = Depends(oauth2.get_current_user)):

    # Check if the current user is an admin
    if current_user.role == 'admin':
        # If the user is an admin, retrieve all appointments
        appointments = db.query(models.Appointment).all()
        return appointments

    else:
        # If the user is not an admin, retrieve appointments associated with the user
        appointments = db.query(models.Appointment).filter(models.Appointment.user_fkey == current_user.id).all()
        return appointments
    


########################### GET APPOINTMENT WITH ID [ READ ] ###########################
@router.get("/{appointment_id}", response_model=schemas.AppointmentResponseData)
def get_clinic(appointment_id: int, db: Session = Depends(get_db), 
               current_user: dict = Depends(oauth2.get_current_user)):
    
    # Retrieve a appointment with the specified ID from the database
    appointment_query = db.query(models.Appointment).filter(models.Appointment.appointments_id == appointment_id)
    appointment = appointment_query.first()

    # If appointment is not found, raise a not found exception
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Appointment with ID: {appointment_id}, not found!")
    
    if appointment.user_fkey != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You don't have permission to view this appointment")

    # Return the appointment
    return appointment


########################### UPDATE APPOINTMENT [ UPDATE ] ###########################
@router.put("/{appointment_id}", response_model=schemas.AppointmentResponseData)
def update_appointment(appointment_id: int, appointment_update: schemas.AppointmentUpdate, db: Session = Depends(get_db),
                       current_user: dict = Depends(oauth2.get_current_user)):
    
    """
    Update an existing appointment.
    """
    # Query the appointment by its ID
    appointment_query = db.query(models.Appointment).filter(models.Appointment.appointments_id == appointment_id)
    appointment = appointment_query.first()

    # Check if the appointment exists
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Appointment with ID: {appointment_id}, not found!")
    
    # Check if the current user has permission to update the appointment
    if appointment.user_fkey != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You don't have permission to update this appointment")
    
    # Prepare appointment data for update, excluding unset fields
    appointment_data = appointment_update.model_dump(exclude_unset=True)

    if "patient_id" in appointment_data:
        patient = db.query(models.Patient).filter(models.Patient.id == appointment_data["patient_id"]).first()
        if not patient:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Invalid patient_id")
        appointment_data["patient_fkey"] = patient.id

    if "doctor_id" in appointment_data:
        doctor = db.query(models.Doctor).filter(models.Doctor.id == appointment_data["doctor_id"]).first()
        if not doctor:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Invalid doctor_id")
        appointment_data["doctor_fkey"] = doctor.id

    if "clinic_id" in appointment_data:
        clinic = db.query(models.Clinic).filter(models.Clinic.id == appointment_data["clinic_id"]).first()
        if not clinic:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Invalid clinic_id")
        appointment_data["clinic_fkey"] = clinic.id

    ################ check avaliability of doctor ####################
    doc_schedule = db.query(models.DoctorSchedule).filter(models.DoctorSchedule.doctor_id == appointment_update.doctor_id).first()

    # Check if the doctor's schedule exists
    if not doc_schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Booking for {doctor.name} is currently unavailable")

    # Fetch all existing appointments
    all_appointments = db.query(models.Appointment).all()
    doctors_ids_arr = [appointment.doctor_id for appointment in all_appointments]
    appointment_date_time_set = {(appointment.appointment_date, appointment.appointment_time) for appointment in all_appointments}
    
    # Check if doctor is already booked
    is_doctor_booked = (appointment_update.doctor_id in doctors_ids_arr) and \
                       ((appointment_update.appointment_date, appointment_update.appointment_time) in appointment_date_time_set)
    

    # Check if the chosen appointment date is within the doctor's schedule date
    if appointment_update.appointment_date != doc_schedule.date:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{doctor.name} does not have a schedule for this date: {appointment_update.appointment_date}."
        )

    # Check if the chosen appointment time is within the doctor's available time slots
    if appointment_update.appointment_time not in doc_schedule.slots:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{doctor.name} has time schedules for these times: {doc_schedule.slots}."
        )
    
    # Check if the chosen clinic is the same as the one where the doctor has a schedule
    if appointment_update.clinic_id != doc_schedule.clinic_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{doctor.name} does not have a schedule at {clinic.name}."
        )
    
    # Check if the doctor is already booked for the chosen date and time
    if is_doctor_booked:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{doctor.name} is already booked for this timeframe")
    ################ end check avaliability of doctor ################

    # Update the appointment data in the database
    appointment_query.update(appointment_data, synchronize_session=False)

    # Commit the changes and refresh the appointment object
    db.commit()
    db.refresh(appointment)

    return appointment


########################### DELETE APPOINTMENT [ DELETE ] ###########################
@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db),
                  current_user: dict = Depends(oauth2.get_current_user)):
    appointment_query = db.query(models.Appointment).filter(models.Appointment.appointments_id == appointment_id)
    appointment = appointment_query.first()

    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Clinic with ID: {id}, not found!")

    # Check if the user is an admin
    if appointment.user_fkey != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You don't have permission to delete this appointment")

    appointment_query.delete(synchronize_session=False)

    # Commit the transaction to the database
    db.commit()

    # Return a response with no content (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

