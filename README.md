# Healthcare Booking Appointment API

This API provides endpoints for booking, managing, and viewing healthcare appointments.

## Frameworks and Tools

The API was built using the following frameworks and tools:

- [FastAPI](https://fastapi.tiangolo.com/): A modern, fast, web framework for building APIs with Python 3.7+ based on standard Python type hints.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/): A database migration tool for SQLAlchemy, allowing you to manage changes to your database schema over time.
- [PostgreSQL](https://www.postgresql.org/): A powerful, open-source relational database management system.
- [SQLAlchemy](https://www.sqlalchemy.org/): A SQL toolkit and Object-Relational Mapping (ORM) library for Python.

## Endpoints

### 1) Create Appointment

**Method:** POST
**Endpoint:** `/appointments`
**Description:** Create a new appointment.

### 2) Update Appointment

**Method:** PUT
**Endpoint:** `/appointments/{appointment_id}`
**Description:** Update an existing appointment.

### 3) View Appointments

**Method:** GET
**Endpoint:** `/appointments`
**Description:** View a list of appointments based on filters (patient_id, doctor_id, date range, etc.).

### 4) Cancel Appointment

**Method:** DELETE
**Endpoint:** `/appointments/{appointment_id}`
**Description:** Cancel an existing appointment.

### 5) User Registration

**Method:** POST
**Endpoint:** `/users`
**Description:** Register a new user account.

### 6) User Login

**Method:** POST
**Endpoint:** `/login`
**Description:** Log in and receive an access token for API interactions.

### 7) Doctor Registration

**Method:** POST
**Endpoint:** `/doctors`
**Description:** Register a new doctor account.

### 8) Clinic Registration

**Method:** POST
**Endpoint:** `/clinics`
**Description:** Register a new clinic.

### 9) View Doctor's Schedule

**Method:** GET
**Endpoint:** `/doctors/{doctor_id}/schedules`
**Description:** View the availability schedule of a specific doctor.

### 10) View All Doctors

**Method:** GET
**Endpoint:** `/doctors`
**Description:** View a list of all doctors.

### 11) View All Clinics

**Method:** GET
**Endpoint:** `/clinics`
**Description:** View a list of all clinics.

### 12) Register Patient

**Method:** POST
**Endpoint:** `/patients`
**Description:** Register a new patient.

### 13) View All Patients

**Method:** GET
**Endpoint:** `/patients`
**Description:** View a list of all registered patients.

## How to Run Locally

1. Clone this repository:
   
```
git clone https://github.com/DavidDanso/healthcare-booking-appointment-api.git
```

```
cd healthcare-booking-appointment-api
```


2. Set up a virtual environment to isolate project dependencies:

On Windows
```
python -m venv venv
```

On macOS and Linux
```
python3 -m venv venv
```

2.1. Activate the virtual environment:

On Windows
```
venv\Scripts\activate
```

On macOS and Linux
```
source venv/bin/activate
```


3. Install FastAPI with all dependencies or install all the packages in the requirements.txt file:

```
pip install fastapi[all]
```

```
pip install -r requirements.txt
```


4. Run the API using uvicorn:

```
uvicorn app.main:app --reload
```


5. Access the API documentation by visiting the following URL in your browser:

```
http://127.0.0.1:8000/docs
```


## Setting Up Database

1. Create a PostgreSQL database.
2. Create a file named .env in the project directory and add the following configuration:

```
DATABASE_HOSTNAME = localhost
DATABASE_PORT = 5432
DATABASE_PASSWORD = your_database_password
DATABASE_NAME = your_database_name
DATABASE_USERNAME = your_database_username
SECRET_KEY = your_secret_key
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60
```

Replace your_database_password, your_database_name, your_database_username, and your_secret_key with appropriate values.

## YouTube Learning Resource

You can learn more about FastAPI by watching the tutorial series on YouTube:

[FastAPI Tutorial Playlist](https://www.youtube.com/watch?v=Yw4LmMQXXFs&list=PL8VzFQ8k4U1L5QpSapVEzoSfob-4CR8zM&index=2)

DavidDanso - davidkellybrownson@gmail.com

