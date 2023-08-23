from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import sessionmaker
from datetime import time
from .config import app_settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{app_settings.DATABASE_USERNAME}:{app_settings.DATABASE_PASSWORD}@{app_settings.DATABASE_HOSTNAME}/{app_settings.DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# postgres database connection
while True:
    try:
        conn = psycopg2.connect(host=app_settings.DATABASE_HOSTNAME, user=app_settings.DATABASE_USERNAME, password=app_settings.DATABASE_PASSWORD, database=app_settings.DATABASE_NAME, 
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connecting to healthcare-appointment database Successful✅")
        break
    except:
        print("Connection to healthcare-appointment database failed❌")
        time.sleep(2)
