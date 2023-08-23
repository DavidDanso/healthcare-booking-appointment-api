from typing import List
from fastapi import Depends, Response, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/clinics'
)

########################### ADD NEW CLINIC [ CREATE ] ###########################
@router.post("/", response_model=schemas.ClinicResponseData, status_code=status.HTTP_201_CREATED)
def add_clinic(clinic: schemas.ClinicCreate, db: Session = Depends(get_db),
               current_user: dict = Depends(oauth2.get_current_user)):
    # Check if the user is an admin
    isAdmin = current_user.role == 'admin'

    if isAdmin:
        # Create a new Clinic object from the provided data
        new_clinic = models.Clinic(**clinic.dict())
        all_clinics = db.query(models.Clinic).all()

        # Check if clinic's name is already in the database.
        if clinic.name in [cli.name for cli in all_clinics]:
            # Raise a Forbidden error if the clinic is already in the database.
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail=f"This Clinic is already in the database.")

        # Add the new clinic to the database session
        db.add(new_clinic)

        # Commit the transaction to the database
        db.commit()

        # Refresh the object in the session to get the updated state from the database
        db.refresh(new_clinic)

        # Return the newly created clinic
        return new_clinic
    else:
        # If user is not an admin, raise a forbidden exception
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only admin can add new clinic.")

########################### GET ALL CLINICS [ READ ] ###########################
@router.get("/", response_model=List[schemas.ClinicResponseData])
def get_clinics(db: Session = Depends(get_db)):
    # Retrieve all clinics from the database
    all_clinics = db.query(models.Clinic).all()

    # Return the list of clinics
    return all_clinics

########################### GET CLINIC WITH ID [ READ ] ###########################
@router.get("/{clinic_id}", response_model=schemas.ClinicResponseData)
def get_clinic(clinic_id: int, db: Session = Depends(get_db)):
    # Retrieve a clinic with the specified ID from the database
    clinic = db.query(models.Clinic).filter(models.Clinic.id == clinic_id).first()

    # If clinic is not found, raise a not found exception
    if not clinic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Clinic with ID: {clinic_id}, not found!")

    # Return the clinic
    return clinic

########################### UPDATE CLINIC [ UPDATE ] ###########################
@router.put("/{clinic_id}", response_model=schemas.ClinicResponseData)
def update_clinic(clinic_id: int, clinic_update: schemas.ClinicUpdate, db: Session = Depends(get_db),
                  current_user: dict = Depends(oauth2.get_current_user)):
    # Query the database for the clinic with the specified ID
    clinic_query = db.query(models.Clinic).filter(models.Clinic.id == clinic_id)

    # If clinic is not found, raise a not found exception
    if not clinic_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Clinic with ID: {clinic_id}, not found!")

    # Check if the user is an admin
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Only admin can update a clinic")

    # Update the clinic's attributes with the provided data
    clinic_query.update(clinic_update.model_dump(exclude_unset=True), synchronize_session=False)

    # Commit the transaction to the database
    db.commit()

    # Refresh the clinic object in the session to get the updated state from the database
    db.refresh(clinic_query.first())

    # Return the updated clinic
    return clinic_query.first()

########################### DELETE CLINIC [ DELETE ] ###########################
@router.delete("/{clinic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clinic(clinic_id: int, db: Session = Depends(get_db),
                  current_user: dict = Depends(oauth2.get_current_user)):
    # Query the database for the clinic with the specified ID
    clinic_query = db.query(models.Clinic).filter(models.Clinic.id == clinic_id)
    clinic = clinic_query.first()

    # If clinic is not found, raise a not found exception
    if not clinic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Clinic with ID: {clinic_id}, not found!")

    # Check if the user is an admin
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Only admin can delete a clinic")

    # Delete the clinic from the database
    clinic_query.delete(synchronize_session=False)

    # Commit the transaction to the database
    db.commit()

    # Return a response with no content (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

