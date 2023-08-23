from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, utils, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/login'
)

########################### LOGIN USER ###########################
@router.post("/", response_model=schemas.Token)
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Query the database to get the user by their email.
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # Check if the user exists. If not, raise a 403 Forbidden HTTPException.
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid Credential")
    
    # Verify the user's password against the stored hashed password.
    # If the password is invalid, raise a 403 Forbidden HTTPException.
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid Credential")
    
    # If the user is authenticated, create an access token for them.
    # The access token is based on the user's username and will be used for future API requests.
    access_token = oauth2.create_access_token(data={"username": user.username})
    
    # Return the access token along with the token type.
    return {"access_token": access_token, "token_type": "bearer"}
