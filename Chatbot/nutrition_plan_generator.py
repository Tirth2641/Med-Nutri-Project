import os
import google.generativeai as genai
import json
import re
from Chatbot.plan_sender import json_to_mealplan_pdf

# Load API key securely
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY :
    raise ValueError("Error: API key is missing. Please set GEMINI_API_KEY.")

# Configure Gemini AI
genai.configure(api_key=API_KEY)
MODEL = genai.GenerativeModel("gemini-2.0-flash")


def generate_gemini_response(prompt: str) -> dict :
    """Generates content from Gemini API."""
    try :
        response = MODEL.generate_content(prompt)

        if response and hasattr(response, 'to_dict') :
            return response.to_dict()

        if response and hasattr(response, 'text') :
            raw_text = response.text.strip()
            if raw_text :
                try :
                    return json.loads(raw_text)  # Try parsing text directly
                except json.JSONDecodeError :
                    return {"error" : "Response received but failed to parse JSON."}

        return {"error" : "No valid response from Gemini API."}

    except Exception as e :
        return {"error" : f"API request failed: {e}"}


def extract_clean_meal_plan(data: dict) -> dict :
    """Extracts and cleans the meal plan from API response."""
    try :
        candidates = data.get("candidates", [])
        if not candidates :
            return {"error" : "Meal plan data missing from response."}

        content_parts = candidates[0].get("content", {}).get("parts", [])
        if not content_parts :
            return {"error" : "Meal plan content missing in API response."}

        raw_text = content_parts[0].get("text", "")

        if not raw_text :
            return {"error" : "Empty meal plan data received."}

        print("Raw API Response:", raw_text)  # Debugging step

        # Remove ```python markers and unwanted text safely
        cleaned_text = re.sub(r"```python\s*", "", raw_text).strip()

        # Parse cleaned text into JSON
        return json.loads(cleaned_text)

    except json.JSONDecodeError :
        return {"error" : "Failed to decode meal plan JSON."}
    except Exception as e :
        return {"error" : f"Unexpected error: {e}"}


def generate_plan(age: int, gender: str, height: float, weight: float,
                  food_pref: str, purpose: str, exercise: str, disease: str) -> dict :
    """Generates a structured meal plan based on user input."""
    prompt = (
        f"Generate a structured meal plan for a {age}-year-old {gender}, {height}m tall, "
        f"weighing {weight}kg, following a {food_pref} diet with {exercise} exercise. "
        f"They have {disease} and their goal is {purpose}. "
        "Provide ONLY the meal plan in a Python dictionary format, without extra information."
    )

    Plan = generate_gemini_response(prompt)
    return extract_clean_meal_plan(Plan)

