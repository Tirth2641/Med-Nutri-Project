import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# --------- Secure Database Setup ---------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mednutri.db")  # Swap with MySQL URL if needed

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread" : False}, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


# --------- Models ---------
class Doctor(Base) :
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


class MedicationPlan(Base) :
    __tablename__ = "medication_plans"
    id = Column(Integer, primary_key=True)
    patient_name = Column(String, nullable=False)
    medicine = Column(String, nullable=False)
    approved = Column(Boolean, default=False)


class NutritionPlan(Base) :
    __tablename__ = "nutrition_plans"
    id = Column(Integer, primary_key=True)
    patient_name = Column(String, nullable=False)
    diet = Column(String, nullable=False)
    approved = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)


# --------- Lifespan Event Handler ---------
@asynccontextmanager
async def lifespan(app: FastAPI) :
    """Handles database initialization and seed data setup."""
    with SessionLocal() as db :
        if not db.query(Doctor).first() :
            db.add_all([
                Doctor(name="Dr. Smith", email="smith@mednutri.com"),
                Doctor(name="Dr. Alice", email="alice@mednutri.com")
            ])
            db.add_all([
                MedicationPlan(patient_name="John", medicine="Paracetamol"),
                MedicationPlan(patient_name="Emma", medicine="Ibuprofen"),
                NutritionPlan(patient_name="John", diet="High Protein"),
                NutritionPlan(patient_name="Emma", diet="Low Carb")
            ])
            db.commit()
    yield


# --------- App Initialization ---------
app = FastAPI(lifespan=lifespan)

# --------- CORS Middleware ---------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------- Dependency Injection for DB Session ---------
def get_db() :
    with SessionLocal() as db :
        yield db


# --------- Schemas ---------
class DoctorSchema(BaseModel) :
    name: str
    email: str


class PlanApproval(BaseModel) :
    plan_id: int
    type: str  # 'medication' or 'nutrition'


# --------- Endpoints ---------
@app.get("/api/doctors")
def get_doctors(db: Session = Depends(get_db)) :
    """Retrieves all doctors."""
    return db.query(Doctor).all()


@app.post("/api/add-doctor")
def add_doctor(data: DoctorSchema, db: Session = Depends(get_db)) :
    """Adds a new doctor to the database."""
    if db.query(Doctor).filter(Doctor.email == data.email).first() :
        raise HTTPException(status_code=400, detail="❌ Doctor with this email already exists")

    doctor = Doctor(name=data.name, email=data.email)
    db.add(doctor)
    db.commit()

    return {"message" : f"✅ Doctor {data.name} added successfully"}


@app.get("/api/logout")
def logout() :
    """Handles user logout."""
    return {"message" : "👋 Successfully logged out"}


@app.get("/api/doctor/plans")
def get_plans(db: Session = Depends(get_db)) :
    """Retrieves unapproved medication and nutrition plans."""
    return {
        "medications" : [
            {"id" : m.id, "patient_name" : m.patient_name, "medicine" : m.medicine}
            for m in db.query(MedicationPlan).filter(MedicationPlan.approved == False).all()
        ],
        "nutritions" : [
            {"id" : n.id, "patient_name" : n.patient_name, "diet" : n.diet}
            for n in db.query(NutritionPlan).filter(NutritionPlan.approved == False).all()
        ]
    }


@app.post("/api/approve-plan")
def approve_plan(data: PlanApproval, db: Session = Depends(get_db)) :
    """Approves a medication or nutrition plan."""
    plan_class = MedicationPlan if data.type == "medication" else NutritionPlan

    plan = db.query(plan_class).filter(plan_class.id == data.plan_id).first()
    if not plan :
        raise HTTPException(status_code=404, detail="Plan not found")

    plan.approved = True
    db.commit()

    return {"message" : f"✅ {data.type.title()} plan approved"}


# --------- Run the App ---------
if __name__ == "__main__" :
    uvicorn.run("Mednutri_app:app", host="127.0.0.1", port=8000, reload=True)
