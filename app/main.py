# Import required modules and components
from fastapi import FastAPI
from . import models
from .config import app_settings
from .database import engine
from fastapi.middleware.cors import CORSMiddleware
from .routers import doctors, users, auth, patients, clinics, schedules, appointments

# Create database tables based on models defined in 'models'
# models.Base.metadata.create_all(bind=engine)

# Create a FastAPI application instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

###################### INCLUDE ROUTERS * #####################

# Import and include the routers defined in the respective modules into the FastAPI application

# Include the 'users' router for user-related endpoints
app.include_router(users.router)

# Include the 'doctors' router for doctor-related endpoints
app.include_router(doctors.router)

# Include the 'auth' router for authentication and authorization endpoints
app.include_router(auth.router)

# Include the 'patients' router for patient-related endpoints
app.include_router(patients.router)

# Include the 'clinics' router for clinic-related endpoints
app.include_router(clinics.router)

# Include the 'schedules' router for appointment scheduling endpoints
app.include_router(schedules.router)

# Include the 'appointments' router for appointment scheduling endpoints
app.include_router(appointments.router)

# Define a root endpoint that responds to HTTP GET requests at the base URL ("/")

@app.get("/")
def read_root():
    """
    Root Endpoint

    Returns a simple response indicating the name of the healthcare appointment booking API.

    Returns:
        dict: A dictionary containing the response message.
    """
    return {"response": "healthcare-appointment-booking-api"}

