from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse
import random
from Chatbot.nutrition_plan_generator import generate_plan
from Chatbot.patients_db import add_patient, get_patients_for_dialogflow, select_patients
from Chatbot.user_verify import generate_otp, verify_otp
from Chatbot.Nutrition_Medication_db import add_plan, add_reminder
from Chatbot.plan_sender import telegram_plan_sender

webhook_router = APIRouter()


# Utility functions for generating IDs
def generate_id(prefix) :
    return f"{prefix}{random.randint(1000, 9999)}"


# Intent handlers
def handle_phone_number(payload) :
    chat_id = payload['originalDetectIntentRequest']['payload']['data']['chat']['id']
    phone_number = payload['queryResult']['queryText']
    return generate_otp(f"+91{phone_number}")


def handle_otp_verification(payload) :
    phone_number = payload['queryResult']['queryText']
    otp = str(payload['queryResult']['queryText'])
    return verify_otp(f"+91{phone_number}", otp)


def handle_existing_user(payload) :
    phone_number = payload['queryResult']['queryText']
    return JSONResponse(content={"fulfillmentText" : f"{get_patients_for_dialogflow(phone_number)}"})


def handle_new_patient(parameters, user_info) :
    patient_id = generate_id("patient")
    user_info.update({
        "pid" : patient_id,
        "Name" : parameters['person']['name'],
        "Age" : int(parameters['age']['amount']),
        "Gender" : parameters['Gender'],
        "phone_number" : user_info.get("phone_number"),
    })

    if add_patient(**user_info) :
        msg = f"{user_info['Name']} has been successfully registered with patient id {patient_id}🎉"
    else :
        msg = f"Registration failed for {user_info['Name']}. Please try again."

    return JSONResponse(content={"fulfillmentText" : msg})


@webhook_router.post("/")
async def handle_request(request: Request) :
    payload = await request.json()
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']

    intent_mapping = {
        "Phone_Number" : handle_phone_number,
        "OTP_Verification" : handle_otp_verification,
        "Existing-User" : handle_existing_user,
        "New-User-3-Options" : lambda p : handle_new_patient(parameters, {}),
    }

    return intent_mapping.get(intent, lambda _ : {"message" : "Invalid intent"})(payload)
