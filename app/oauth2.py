from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from . import schemas, models
from . database import get_db
from fastapi.security import OAuth2PasswordBearer

# Define the secret key for encoding and decoding JWT tokens.
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

# Specify the algorithm used for encoding and decoding JWT tokens.
ALGORITHM = "HS256"

# Define the expiration time for access tokens, in minutes.
ACCESS_TOKEN_EXPIRE_MINUTES = 120

# Create an OAuth2 scheme for password bearer token authentication.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Function to create an access token by encoding a payload with expiration time.
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify an access token and extract user data from it.
def verify_access_token(token: str, credentials_exception):
    try:
        # Decode the JWT token using the provided secret key and algorithm.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        
        # If username is missing in the token, raise an exception.
        if username is None:
            raise credentials_exception
        
        # Create a TokenData object containing the username.
        token_data = schemas.TokenData(username=username)
    except JWTError:
        # If decoding fails, raise an exception.
        raise credentials_exception
    return token_data

# Function to get the current user based on the provided access token and database session.
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Create an exception to handle unauthorized access.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verify the access token and get token data (username).
    token = verify_access_token(token, credentials_exception)
    
    # Query the database to get the user associated with the username.
    user = db.query(models.User).filter(models.User.username == token.username).first()
    
    # Return the user object.
    return user
