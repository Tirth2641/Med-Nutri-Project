import requests
import os
from fpdf import FPDF

# Secure API key handling
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Error: Bot token is missing. Set TELEGRAM_BOT_TOKEN as an environment variable.")

def json_to_mealplan_pdf(json_data, pdf_filename="single_day_meal_plan.pdf"):
    """
    Converts a meal plan JSON into a well-formatted PDF.
    """
    try:
        meal_plan = json_data.get("meal_plan", {})

        # Initialize PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add header
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(0, 10, "Meal Plan", ln=True, align="C")
        pdf.ln(10)

        # Function to format meal sections
        def add_meal_section(meal_time, meal_details):
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(0, 10, f"{meal_time.capitalize()}:", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, "\n".join([
                f"  Name: {meal_details.get('name', 'N/A')}",
                f"  Description: {meal_details.get('description', 'N/A')}",
                f"  Calories: {meal_details.get('calories', 'N/A')}",
                f"  Protein: {meal_details.get('protein', 'N/A')}g",
                f"  Carbs: {meal_details.get('carbs', 'N/A')}g",
                f"  Fat: {meal_details.get('fat', 'N/A')}g",
            ]))
            pdf.ln(5)

        # Process meals
        for meal_time, meal_details in meal_plan.items():
            if meal_time not in ["total_calories", "total_protein", "total_carbs", "total_fat"]:
                add_meal_section(meal_time, meal_details)

        # Nutritional Summary
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(0, 10, "Nutritional Summary", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, "\n".join([
            f"  Total Calories: {meal_plan.get('total_calories', 'N/A')}",
            f"  Total Protein: {meal_plan.get('total_protein', 'N/A')}g",
            f"  Total Carbs: {meal_plan.get('total_carbs', 'N/A')}g",
            f"  Total Fat: {meal_plan.get('total_fat', 'N/A')}g",
        ]))

        # Save PDF
        pdf.output(pdf_filename)
        print(f"PDF created successfully: {pdf_filename}")

    except Exception as e:
        print(f"Error generating PDF: {e}")

def send_pdf_to_telegram(chat_id, text_message, pdf_file_path):
    """
    Sends the generated meal plan PDF to Telegram.
    """
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

        with open(pdf_file_path, "rb") as pdf_file:
            response = requests.post(url, data={"chat_id": chat_id, "caption": text_message}, files={"document": pdf_file})

        if response.status_code == 200:
            print("PDF successfully sent!")
        else:
            print(f"Failed to send PDF. Status: {response.status_code}, Response: {response.text}")

    except Exception as e:
        print(f"Error sending PDF to Telegram: {e}")

def telegram_plan_sender(chat_id, json_example):
    """
    Generates and sends a nutrition plan PDF via Telegram.
    """
    pdf_filename = f"Nutrition_plan_{chat_id}.pdf"
    json_to_mealplan_pdf(json_example, pdf_filename)
    send_pdf_to_telegram(chat_id, "Here is your meal plan PDF!", pdf_filename)
