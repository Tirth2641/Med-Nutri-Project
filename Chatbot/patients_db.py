import os
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from fastapi.responses import JSONResponse

# Secure database connection handling
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:2641@127.0.0.1:3306/mednutri")

# Create database engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)

# Create a base class for ORM models
Base = declarative_base()

# Define the Patients table
class Patient(Base):
    __tablename__ = 'patients'
    pid = Column(String(255), primary_key=True)
    Name = Column(String(255), nullable=False)
    Mobile = Column(String(255), nullable=False)
    Age = Column(Integer, nullable=False)
    Gender = Column(String(255), nullable=False)

# Create tables if they don't exist
Base.metadata.create_all(engine)

# Create a session factory
SessionLocal = sessionmaker(bind=engine)

def get_db_session():
    """Provides a database session for safe transaction handling."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def add_patient(pid: str, Name: str, Mobile: str, Age: int, Gender: str):
    """Adds a new patient to the database."""
    session = SessionLocal()
    try:
        new_patient = Patient(pid=pid, Name=Name, Mobile=Mobile, Age=Age, Gender=Gender)
        session.add(new_patient)
        session.commit()
        print(f"✅ Patient added successfully: {Name} ({pid})")
        return True
    except Exception as e:
        session.rollback()
        print(f"❌ Error adding patient: {e}")
        return False
    finally:
        session.close()

def get_patients_for_dialogflow(Mobile: str):
    """Retrieves patients linked to a mobile number."""
    session = SessionLocal()
    try:
        patients = session.query(Patient.pid, Patient.Name, Patient.Age, Patient.Gender).filter(
            Patient.Mobile == Mobile).all()

        if not patients:
            return "⚠️ No patients found with this mobile number."

        response_lines = ["**Patients linked to this mobile number:**\n"]
        for patient in patients:
            response_lines.append(f"\n🔹 **Patient ID:** {patient.pid}")
            response_lines.append(f"📌 **Name:** {patient.Name}")
            response_lines.append(f"🎂 **Age:** {patient.Age} years")
            response_lines.append(f"⚧ **Gender:** {patient.Gender}")
            response_lines.append("───────────────────── \n")

        response_lines.append("Select a patient ID:")
        return "\n".join(response_lines)

    finally:
        session.close()

async def select_patients(pid: str):
    """Fetches a patient’s details based on their ID."""
    session = SessionLocal()
    try:
        return session.query(Patient).filter(Patient.pid == pid).first()
    finally:
        session.close()
