import os
import random
from fastapi import FastAPI, HTTPException, APIRouter, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext

# Secure database setup
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:2641@localhost/mednutri")
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

signup_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Dependency Injection for DB Session
def get_db() :
    with SessionLocal() as db :
        yield db


# Models
class User(Base) :
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    mobile = Column(String(20), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Store hashed passwords
    user_type = Column(String(50), nullable=False)


class Patient(Base) :
    __tablename__ = "patients"
    pid = Column(String(255), primary_key=True)
    Name = Column(String(255), nullable=False)
    Mobile = Column(String(255), unique=True, nullable=False)
    Age = Column(Integer, nullable=False)
    Gender = Column(String(255), nullable=False)


Base.metadata.create_all(bind=engine)


# Pydantic Schema
class SignupModel(BaseModel) :
    name: str
    email: EmailStr
    mobile: str
    password: str
    user_type: str
    age: int | None = None
    gender: str | None = None


def hash_password(password) :
    """Hashes a password for secure storage."""
    return pwd_context.hash(password)


@signup_router.post("/auth/signup/")
async def signup(data: SignupModel, db: Session = Depends(get_db)) :
    """Handles patient and user registration securely."""
    print("Received data:", data)

    if db.query(User).filter(User.email == data.email).first() or db.query(Patient).filter(
            Patient.Mobile == data.mobile).first() :
        raise HTTPException(status_code=400, detail="❌ User or patient with this email/mobile already exists")

    if data.user_type.lower() == "patient" :
        pid = f"patient{random.randint(1000, 9999)}"
        new_patient = Patient(pid=pid, Name=data.name, Mobile=data.mobile, Age=data.age, Gender=data.gender)
        db.add(new_patient)
        db.commit()
        return {"success" : True, "message" : "🎉 Patient registered successfully"}

    new_user = User(
        name=data.name,
        email=data.email,
        mobile=data.mobile,
        password=hash_password(data.password),  # Secure password storage
        user_type=data.user_type,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"success" : True, "message" : "🎉 User registered successfully"}
