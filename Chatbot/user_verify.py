import os
import random
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from twilio.rest import Client
import time

# Load Twilio credentials securely
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]) :
    raise ValueError("Error: Twilio credentials are missing. Set them as environment variables.")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Temporary OTP storage with expiry timestamps
otp_storage = {}


def generate_otp(phone_number: str) :
    """Generates a secure OTP and sends it via Twilio."""
    otp = str(random.randint(100000, 999999))
    otp_storage[phone_number] = {"otp" : otp, "expires_at" : time.time() + 300}  # OTP expires in 5 minutes

    try :
        message = client.messages.create(
            body=f"🔑 Your MedNutri verification code is {otp}. It expires in 5 minutes.",
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return JSONResponse(content={"fulfillmentText" : f"✅ OTP sent to {phone_number}. Please enter it to verify."})

    except Exception as e :
        return JSONResponse(content={"error" : f"❌ Failed to send OTP: {e}"}, status_code=500)


def verify_otp(phone_number: str, otp: str) :
    """Verifies OTP within the valid time window."""
    stored_data = otp_storage.get(phone_number)

    if stored_data and stored_data["otp"] == otp :
        if time.time() > stored_data["expires_at"] :
            del otp_storage[phone_number]  # Cleanup expired OTP
            raise HTTPException(status_code=400, detail="⏳ OTP expired. Please request a new one.")

        del otp_storage[phone_number]  # Remove OTP after successful verification
        return JSONResponse(content={
            "fulfillmentText" : "🎉 OTP verified! Welcome to MedNutri. Would you like to continue as an existing member or add a new member?"})

    raise HTTPException(status_code=400, detail="⚠️ Invalid OTP. Please try again.")
