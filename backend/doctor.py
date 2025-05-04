import os
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ========== Secure Database Setup ==========
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:2641@127.0.0.1:3306/mednutri")
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ========== Model ==========
class Doctor(Base) :
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)


# ========== Create Tables ==========
Base.metadata.create_all(bind=engine)


# ========== DB Dependency ==========
def get_db() :
    """Provides a database session for safe transaction handling."""
    with SessionLocal() as db :
        yield db


# ========== Pydantic Schemas ==========
class DoctorCreate(BaseModel) :
    name: str
    email: str


# ========== Router ==========
doctor_router = APIRouter()


@doctor_router.get("/api/doctors")
def get_doctors(db: Session = Depends(get_db)) :
    """Retrieves all doctors."""
    return db.query(Doctor).all()


@doctor_router.post("/api/add-doctor")
def add_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)) :
    """Adds a new doctor to the database."""
    if db.query(Doctor).filter(Doctor.email == doctor.email).first() :
        raise HTTPException(status_code=400, detail="❌ Doctor already exists")

    new_doc = Doctor(name=doctor.name, email=doctor.email)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return {"message" : f"✅ Doctor {doctor.name} added successfully", "doctor_id" : new_doc.id}


@doctor_router.get("/api/logout")
def logout() :
    """Handles user logout."""
    return {"message" : "👋 Successfully logged out"}
