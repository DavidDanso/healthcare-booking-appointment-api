from typing import List
from fastapi import Depends, Response, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from .. database import get_db

router = APIRouter(
    prefix='/patients'
)

########################### ADD NEW PATIENT [ CREATE ] ###########################
@router.post("/", response_model=schemas.PatientResponseData, status_code=status.HTTP_201_CREATED)
def add_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db),
                current_user: dict = Depends(oauth2.get_current_user)):
    # Create a new Patient instance, associating it with the current user ID
    new_patient = models.Patient(user_id=current_user.id, **patient.dict())

    all_patients = db.query(models.Patient).all()
    patients_ids_arr = [patient_data.name for patient_data in all_patients]

    # Check if doctor_id is already in the database.
    if patient.name in patients_ids_arr:
        # Raise a Forbidden error if the doctor is already booked.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"The information of '{patient.name}' has been successfully added already.")
    
    db.add(new_patient)  # Add the new patient to the database
    db.commit()  # Commit the transaction
    db.refresh(new_patient)  # Refresh the instance to ensure its attributes are up-to-date

    return new_patient  # Return the newly created patient

########################## GET PATIENT WITH ID [ READ ] ###########################
@router.get("/{patient_id}", response_model=schemas.PatientResponseData)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    # Query the database for a patient with the specified ID
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()

    if not patient:
        # If patient doesn't exist, raise a 404 Not Found error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Patient with ID: {patient_id}, not found!")

    return patient  # Return the retrieved patient

########################### GET ALL PATIENTS [ READ ] ###########################
@router.get("/", response_model=List[schemas.PatientResponseData])
def get_patients(db: Session = Depends(get_db), 
                 current_user: dict = Depends(oauth2.get_current_user)):
    
    # Check if the current user is an admin, show all patients.
    if current_user.role == 'admin':
        all_patients = db.query(models.Patient).all()
    else:
        # Query the database to retrieve all patients created by the current user.
        all_patients = db.query(models.Patient).filter(models.Patient.user_id == current_user.id).all()

    return all_patients  # Return the list of all patients

########################### UPDATE PATIENT [ UPDATE ] ###########################
@router.put("/{patient_id}", response_model=schemas.PatientResponseData)
def update_patient(patient_id: int, patient_update: schemas.PatientUpdate, db: Session = Depends(get_db),
                   current_user: dict = Depends(oauth2.get_current_user)):
    # Query the database for the patient to be updated
    patient_query = db.query(models.Patient).filter(models.Patient.id == patient_id)
    patient = patient_query.first()

    if not patient:
        # If patient doesn't exist, raise a 404 Not Found error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Patient with ID: {patient_id} not found!")

    if patient.user_id != current_user.id and current_user.role != 'admin':
        # If the current user is not the owner or an admin, raise a 403 Forbidden error
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You don't have permission to update this patient")

    # Update patient attributes based on the provided update data
    patient_query.update(patient_update.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()  # Commit the transaction

    db.refresh(patient_query.first())  # Refresh the patient instance

    return patient  # Return the updated patient

########################### DELETE PATIENT [ DELETE ] ###########################
@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(patient_id: int, db: Session = Depends(get_db),
                current_user: dict = Depends(oauth2.get_current_user)):
    # Query the database for the patient to be deleted
    patient_query = db.query(models.Patient).filter(models.Patient.id == patient_id)
    patient = patient_query.first()

    if not patient:
        # If patient doesn't exist, raise a 404 Not Found error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Patient with ID: {patient_id} not found!")

    if patient.user_id != current_user.id and current_user.role != 'admin':
        # If the current user is not the owner or an admin, raise a 403 Forbidden error
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You don't have permission to delete this patient")

    patient_query.delete(synchronize_session=False)  # Delete the patient from the database
    db.commit()  # Commit the transaction

    return Response(status_code=status.HTTP_204_NO_CONTENT)  # Return a 204 No Content response

