from fastapi import FastAPI
from backend.signup import signup_router
from backend.login import login_router
from Chatbot.webhook import webhook_router
from backend.doctor import doctor_router
from backend.doctor_dashboard import dashboard_router
from fastapi.middleware.cors import CORSMiddleware
import os

# Initialize FastAPI app
app = FastAPI()

# Load allowed origins dynamically for better security
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Define trusted origins securely
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Limit allowed methods
    allow_headers=["Authorization", "Content-Type"],  # Restrict headers
)

# Include app routers
app.include_router(signup_router, prefix="/auth", tags=["Authentication"])
app.include_router(login_router, prefix="/auth", tags=["Authentication"])
app.include_router(webhook_router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(doctor_router, prefix="/doctor", tags=["Doctor"])
app.include_router(dashboard_router, prefix="/doctor", tags=["Doctor Dashboard"])
