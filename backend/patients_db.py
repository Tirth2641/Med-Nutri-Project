import os
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from fastapi.responses import JSONResponse

# Secure database setup
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:2641@127.0.0.1:3306/mednutri")

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Define the Patients model
class Patient(Base):
    __tablename__ = "patients"
    pid = Column(String(255), primary_key=True)
    Name = Column(String(255), nullable=False)
    Mobile = Column(String(255), unique=True, nullable=False)
    Age = Column(Integer, nullable=False)
    Gender = Column(String(255), nullable=False)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Dependency Injection for DB Session
def get_db():
    with SessionLocal() as db:
        yield db

def add_patient(pid: str, Name: str, Mobile: str, Age: int, Gender: str) -> bool:
    """Adds a new patient to the database."""
    try:
        with SessionLocal() as session:
            new_patient = Patient(pid=pid, Name=Name, Mobile=Mobile, Age=Age, Gender=Gender)
            session.add(new_patient)
            session.commit()
        return True
    except Exception as e:
        print(f"❌ Error adding patient: {e}")
        return False

def get_patients_for_dialogflow(Mobile: str) -> str:
    """Retrieves patients linked to a mobile number."""
    with SessionLocal() as session:
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

def select_patients(pid: str) -> JSONResponse:
    """Fetches a patient’s details based on their ID."""
    with SessionLocal() as session:
        patient = session.query(Patient).filter(Patient.pid == pid).first()

        if patient:
            return JSONResponse(content={
                "fulfillmentText": f"""
                Here are the details you provided:
                🔹 Name: {patient.Name}
                🔹 Age: {patient.Age}
                🔹 Gender: {patient.Gender}

                Everything looks good! 👍 Now, would you like to proceed with:
                🔹 Medication Reminder 💊⏰
                🔹 Nutrition Plan 🥗
                🔹 View History 📊"""
            })
        return JSONResponse(content={"message": "❌ Patient not found"})
