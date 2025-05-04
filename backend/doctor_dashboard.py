import os
import json
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import create_engine, Column, String, Date, Boolean
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
from datetime import date

# Secure database setup
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:2641@127.0.0.1:3306/mednutri")
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

dashboard_router = APIRouter()
today = date.today()


# Define Tables
class NutritionPlan(Base) :
    __tablename__ = "nutrition_plan"
    nid = Column(String(255), primary_key=True)
    plan_name = Column(String(255), nullable=False)
    plan = Column(String(255), nullable=False)  # Store JSON as String
    pid = Column(String(255), nullable=False)
    date = Column(Date, default=today)
    approved = Column(Boolean, default=False)


class MedicationReminder(Base) :
    __tablename__ = "medication_reminder"
    mid = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    reminder = Column(String(255), nullable=False)  # Store JSON as String
    pid = Column(String(255), nullable=False)
    date = Column(Date, default=today)
    approved = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)


# Pydantic Schemas
class ApproveRequest(BaseModel) :
    plan_id: str
    plan_type: str


def convert_to_inner_dict(data) :
    """Safely converts data to a structured dictionary format."""
    try :
        if isinstance(data, str) :
            try :
                return json.loads(data)  # Parse JSON if valid
            except json.JSONDecodeError :
                return {"value" : data}
        if isinstance(data, dict) :
            return {key : convert_to_inner_dict(value) for key, value in data.items()}
        return {"value" : data}
    except Exception as e :
        print(f"Error converting data: {e}")
        return {}


# Dependency Injection for DB Session
def get_db() :
    with SessionLocal() as db :
        yield db


@dashboard_router.get("/api/doctor/plans")
def fetch_plans(db: Session = Depends(get_db)) :
    """Fetches nutrition and medication plans from the database."""
    nutrition_plans = db.query(NutritionPlan).filter(NutritionPlan.date == today).all()
    medication_reminders = db.query(MedicationReminder).filter(MedicationReminder.date == today).all()

    return {
        "nutritions" : [
            {"nid" : plan.nid, "plan_name" : plan.plan_name, "plan" : convert_to_inner_dict(plan.plan),
             "date" : plan.date, "approved" : plan.approved}
            for plan in nutrition_plans
        ],
        "medications" : [
            {"mid" : reminder.mid, "name" : reminder.name, "reminder" : convert_to_inner_dict(reminder.reminder),
             "date" : reminder.date, "approved" : reminder.approved}
            for reminder in medication_reminders
        ]
    }


@dashboard_router.post("/api/approve-plan")
def approve_plan(request: ApproveRequest, db: Session = Depends(get_db)) :
    """Approves a nutrition or medication plan."""
    plan_classes = {"nutrition" : NutritionPlan, "medication" : MedicationReminder}
    plan_class = plan_classes.get(request.plan_type)

    if not plan_class :
        raise HTTPException(status_code=400, detail="Invalid plan type")

    plan = db.query(plan_class).filter(
        plan_class.nid if request.plan_type == "nutrition" else plan_class.mid == request.plan_id).first()
    if not plan :
        raise HTTPException(status_code=404, detail="Plan not found")

    plan.approved = True
    db.commit()
    return {"message" : f"{request.plan_type.capitalize()} plan with ID {request.plan_id} approved successfully"}
