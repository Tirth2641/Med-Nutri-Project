import pandas as pd
import joblib

# Load the trained model and encoders
def load_model():
    model = joblib.load("health_risk_model.pkl")
    label_encoders = joblib.load("label_encoders.pkl")
    return model, label_encoders

# Make a prediction
def make_prediction(sample_data):
    model, label_encoders = load_model()
    sample_df = pd.DataFrame([sample_data])
    prediction = model.predict(sample_df)
    risk_label = label_encoders['Risk'].inverse_transform(prediction)
    return risk_label[0]

# Example test case
sample_patient = {'Age': 45, 'BMI': 27.5, 'Num_Medicines': 3, 'Disease': 1, 'Medication_Frequency': 2}
predicted_risk = make_prediction(sample_patient)
print(f"Predicted Health Risk: {predicted_risk}")
