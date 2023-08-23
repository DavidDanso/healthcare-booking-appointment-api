from typing import List
from fastapi import Depends, Response, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from .. import models, utils, schemas, oauth2
from .. database import get_db

router = APIRouter(
    prefix='/users'
)

########################### ADD NEW USER [ CREATE ] ###########################
@router.post("/", response_model=schemas.UserResponseData, status_code=status.HTTP_201_CREATED)
def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password before storing it in the database
    hash_password = utils.get_password_hash(user.password)
    user.password = hash_password

    # Create a new user object and add it to the database
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

########################### GET ALL USER [ READ ] ###########################
@router.get("/", response_model=List[schemas.UserResponseData])
def get_users(db: Session = Depends(get_db)):
    # Retrieve all user records from the database
    all_users = db.query(models.User).all()

    return all_users


########################## GET USER WITH ID [ READ ] ###########################
@router.get("/{id}", response_model=schemas.UserResponseData)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with ID: {id}, not found!")

    return user

########################### UPDATE USER [ UPDATE ] ###########################
@router.put("/{id}", response_model=schemas.UserResponseData)
def update_user(id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db),
                get_user: dict = Depends(oauth2.get_current_user)):
    
    # Find the user with the given ID
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    # Check if the user exists
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with ID: {id} not found!")
    
    # Check if the authenticated user has permission to update this user
    if get_user.username != user.username and get_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"You don't have permission to update this user")
    
    # Update the user record with the provided data
    user_query.update(user_update.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()

    # Refresh the user object to get the updated data
    db.refresh(user_query.first())

    return user


########################### DELETE USER [ DELETE ] ###########################
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), 
                get_user: dict = Depends(oauth2.get_current_user)):
    # Find the user with the given ID
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    # Check if the user exists
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with ID: {id} not found!")
    
    # Check if the authenticated user has permission to delete this user
    if get_user.username != user.username and get_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"You don't have permission to delete this user")
    
    # Delete the user record
    user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
