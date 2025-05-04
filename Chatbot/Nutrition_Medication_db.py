import os
import json
import traceback
from sqlalchemy import create_engine, Column, String, Integer, Date, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from datetime import date

# Secure database connection handling
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:2641@127.0.0.1:3306/mednutri")

# Create database engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)

# Create base class for ORM models
Base = declarative_base()

# Define Tables
class Nutrition_Plan(Base):
    __tablename__ = 'nutrition_plan'
    nid = Column(String(255), primary_key=True)
    plan_name = Column(String(255), nullable=False)
    plan = Column(String, nullable=False)  # Store JSON as a string for consistency
    pid = Column(String(255), nullable=False)
    date = Column(Date, default=date.today())

class Medication_Reminder(Base):
    __tablename__ = 'medication_reminder'
    mid = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    reminder = Column(String, nullable=False)  # Store JSON as a string
    pid = Column(String(255), nullable=False)
    date = Column(Date, default=date.today())

class Adherence_Record(Base):
    __tablename__ = 'adherence_records'
    ARid = Column(String(255), primary_key=True)
    pid = Column(String(255), nullable=False)
    nid = Column(String(255), nullable=True)
    mid = Column(String(255), nullable=True)
    date = Column(Date, default=date.today())
    created_at = Column(DateTime, default=func.now())

# Create tables if they don't exist
Base.metadata.create_all(engine)

# Create a session factory
SessionLocal = sessionmaker(bind=engine)

def add_plan(nid: str, plan_name: str, plan: dict, pid: str, ARid: str) -> bool:
    """Adds a new nutrition plan and updates adherence record."""
    try:
        with SessionLocal() as session:
            new_plan = Nutrition_Plan(
                nid=nid,
                plan_name=plan_name,
                plan=json.dumps(plan),
                pid=pid
            )
            session.add(new_plan)
            session.flush()

            new_record = Adherence_Record(
                ARid=ARid,
                pid=pid,
                nid=nid,
                mid=None
            )
            session.add(new_record)
            session.commit()

        print("✅ Nutrition Plan added successfully!")
        return True
    except SQLAlchemyError as e:
        print(f"❌ Error adding plan: {e}")
        traceback.print_exc()
        return False

def add_reminder(mid: str, name: str, reminder: dict, pid: str, ARid: str) -> bool:
    """Adds a medication reminder and adherence record."""
    try:
        with SessionLocal() as session:
            reminder_json = json.dumps(reminder)

            new_reminder = Medication_Reminder(
                mid=mid,
                name=name,
                reminder=reminder_json,
                pid=pid
            )
            session.add(new_reminder)
            session.commit()

            new_record = Adherence_Record(
                ARid=ARid,
                pid=pid,
                nid=None,
                mid=mid
            )
            session.add(new_record)
            session.commit()

        print("✅ Reminder and adherence record added successfully!")
        return True
    except SQLAlchemyError as e:
        print(f"❌ Error adding reminder: {e}")
        return False


