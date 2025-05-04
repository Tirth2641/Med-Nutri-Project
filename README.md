# **MedNutri API** 🏥🤖  
_A FastAPI-powered AI-driven healthcare chatbot with Dialogflow and Telegram integration._  

## **📌 Overview**  
MedNutri is an AI-powered chatbot designed to assist with **medication reminders** and **nutrition plans**.  
It integrates **FastAPI**, **Dialogflow**, **Telegram**, **MySQL**, and **ngrok** for webhook exposure, with **Docker** and **Uvicorn** for streamlined deployment.

**This project was developed as part of a final-year internship by:**  
**Tirth Patel (Project Coordinator), Umang Rao, Dhara Dave, Vishakha Rathi, and Rachi Gupta.**

---

## **🚀 Features**
- **Secure authentication** (Signup & Login)
- **Doctor & Patient management**
- **Nutrition & Medication plan approval**
- **Dialogflow webhook integration**
- **Telegram bot connection**
- **MySQL database support**
- **Dockerized deployment with Uvicorn**
- **ngrok for local webhook exposure**

---

## **🔧 Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/Tirth2641/Med-Nutri-Project
cd mednutri

###2️⃣ Install Dependencies
bash
pip install -r requirements.txt

###3️⃣ Set up the Database
Create a MySQL database

sql
CREATE DATABASE mednutri;
Import the .sql file

bash
mysql -u root -p mednutri < mednutri.sql
Update DATABASE_URL in .env file

bash
DATABASE_URL=mysql+pymysql://root:password@localhost/mednutri


###4️⃣ Configure Environment Variables
Rename .env.example to .env and set up:

env
DATABASE_URL=mysql+pymysql://root:password@localhost/mednutri
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=your_number
TELEGRAM_BOT_TOKEN=your_token
ALLOWED_ORIGINS=http://localhost:3000


###5️⃣ Run the Server Locally
bash
uvicorn Mednutri_app:app --host 127.0.0.1 --port 8000 --reload

##🐳 Dockerization
###1️⃣ Build the Docker Image
Create a Dockerfile in the project root:

dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "Mednutri_app:app", "--host", "0.0.0.0", "--port", "8000"]
Then, build the image:

bash
docker build -t mednutri-api .
###2️⃣ Run the Docker Container
bash
docker run -d -p 8000:8000 --env-file .env --name mednutri-container mednutri-api
###3️⃣ Verify the Running Container
bash
docker ps
💻 Connecting Webhook with Dialogflow
Start ngrok:

bash
ngrok http 8000
Copy the ngrok HTTPS URL.

Go to Dialogflow Console → Fulfillment → Webhook.

Paste the URL:

https://your-ngrok-url.ngrok.io/webhook
Click Enable webhook.

##🤖 Connecting Dialogflow with Telegram
###1️⃣ Create a Telegram Bot
Open Telegram and chat with @BotFather.

Send /newbot → Choose bot name and username.

Copy the API token.

###2️⃣ Connect Telegram to Dialogflow
Go to Dialogflow → Integrations → Telegram.

Paste your Telegram bot API token.

Click Enable.




