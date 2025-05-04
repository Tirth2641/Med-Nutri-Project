import os
from fastapi import FastAPI, HTTPException, APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext

# Secure database setup
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:2641@localhost/mednutri")

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

login_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Define User Model
class User(Base) :
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    mobile = Column(String(20), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Store hashed password
    user_type = Column(String(50), nullable=False)


Base.metadata.create_all(bind=engine)


# Pydantic Schemas
class UserLogin(BaseModel) :
    email: str
    password: str
    user_type: str


class UserRegister(BaseModel) :
    name: str
    email: str
    mobile: str
    password: str
    user_type: str


# Dependency Injection for DB Session
def get_db() :
    with SessionLocal() as db :
        yield db


def verify_password(plain_password, hashed_password) :
    """Verifies a password against its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password) :
    """Hashes a password for secure storage."""
    return pwd_context.hash(password)


@login_router.post("/auth/login/")
def login(user: UserLogin, db: Session = Depends(get_db)) :
    """Handles user login by verifying stored credentials."""
    db_user = db.query(User).filter(User.email == user.email, User.user_type == user.user_type).first()

    if not db_user or not verify_password(user.password, db_user.password) :
        raise HTTPException(status_code=401, detail="❌ Invalid credentials")

    return {"message" : f"✅ Login successful", "user_type" : user.user_type}


@login_router.post("/auth/register/")
def register(user: UserRegister, db: Session = Depends(get_db)) :
    """Handles user registration securely by hashing passwords."""
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user :
        raise HTTPException(status_code=400, detail="❌ User already exists")

    hashed_password = hash_password(user.password)
    new_user = User(name=user.name, email=user.email, mobile=user.mobile, password=hashed_password,
                    user_type=user.user_type)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message" : f"🎉 User {user.name} registered successfully"}

