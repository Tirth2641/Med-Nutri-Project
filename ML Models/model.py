import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the dataset
csv_file_path = "final_corrected_synthetic_health_risk_dataset.csv"
df = pd.read_csv(csv_file_path)

# Display dataset info
df.info()

# Encode categorical variables
label_encoders = {}
for col in ['Disease', 'Medication_Frequency', 'Risk']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # Store encoder for later use

# Define features (X) and target (y)
X = df[['Age', 'BMI', 'Num_Medicines', 'Disease', 'Medication_Frequency']]
y = df['Risk']

# Split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the trained model
joblib.dump(model, "health_risk_model.pkl")
print("Model saved as health_risk_model.pkl")

# Save label encoders for decoding predictions
joblib.dump(label_encoders, "label_encoders.pkl")
print("Label encoders saved as label_encoders.pkl")

# Example Prediction
def make_prediction(sample_data):
    sample_df = pd.DataFrame([sample_data], columns=X.columns)
    prediction = model.predict(sample_df)
    risk_label = label_encoders['Risk'].inverse_transform(prediction)
    return risk_label[0]

# Example test case
sample_patient = {'Age': 45, 'BMI': 27.5, 'Num_Medicines': 3, 'Disease': 1, 'Medication_Frequency': 2}
predicted_risk = make_prediction(sample_patient)
print(f"Predicted Health Risk: {predicted_risk}")
