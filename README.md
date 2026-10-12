AI Healthcare Assistant
An AI-powered healthcare assistant that helps analyze patient symptoms, predict possible diseases, read laboratory reports, generate clinical summaries, and store consultation records.

Important: This project is created for educational and research purposes. It is not a replacement for a qualified doctor, medical diagnosis, or professional healthcare advice.

Introduction
The AI Healthcare Assistant is a backend healthcare application built with Python and FastAPI.

The system combines machine learning, artificial intelligence, OCR, and a PostgreSQL database to support doctors and healthcare professionals during patient consultations.

A user can provide patient symptoms, and the system can:

Predict a possible disease.
Calculate a prediction risk percentage.
Upload and read medical laboratory reports.
Extract test names and values from report images.
Generate a short clinical summary for doctors.
Generate a simple Urdu explanation for patients.
Store patient information and consultation history.
Retrieve previously saved patient records.
The goal of this project is to make healthcare data easier to understand and help doctors organize patient information more efficiently.

Main Features
1. Disease Prediction
The system uses a trained machine learning model to analyze symptoms and predict a possible disease.

The prediction response includes:

Predicted disease
Risk or confidence percentage
The model is trained using an XGBoost classification algorithm.

2. Medical Report Analysis
Users can upload a medical laboratory report as an image.

The system uses an AI vision model to extract:

Medical test names
Measured values
Units
Other useful laboratory information
Supported image formats:

PNG
JPG
JPEG
3. AI Clinical Summary
The application generates summaries based on:

Patient symptoms
Predicted disease
Prediction risk percentage
It provides two types of summaries:

A professional English summary for doctors
A simple Urdu summary for patients
This makes medical information easier to understand for both healthcare professionals and patients.

4. Patient Record Management
The project uses PostgreSQL and SQLAlchemy to store healthcare records.

The database can store:

Doctor information
Patient information
Consultation details
Patient symptoms
Disease predictions
Risk percentages
Laboratory report data
AI-generated clinical summaries
5. Consultation History
Saved patient records can be retrieved through the API.

This allows doctors to review previous consultations and patient information.

Technology Stack
Backend
Python
FastAPI
Uvicorn
Pydantic
Machine Learning
XGBoost
Scikit-learn
NumPy
Pandas
Joblib
Artificial Intelligence
Google Gemini API for laboratory report analysis
Groq API for AI-generated summaries
Database
PostgreSQL
SQLAlchemy
PostgreSQL JSONB fields
Image Processing
Pillow
Project Structure
AI-Healthcare-Assistant/
│
├── artifacts/
│   ├── disease_model.pkl
│   ├── label_encoder.pkl
│   └── symptom_features.json
│
├── backend.py
├── database.py
├── init_db.py
├── model_training.py
├── model_training.ipynb
├── models.py
├── report.py
├── sample_lab_report.png
├── .gitignore
└── README.md
File Description
File	Description
backend.py	Contains the FastAPI application and API endpoints
database.py	Creates the SQLAlchemy database connection
models.py	Defines the database tables and relationships
init_db.py	Creates the PostgreSQL database tables
model_training.py	Trains and saves the disease prediction model
model_training.ipynb	Notebook version of the model training process
report.py	Generates a sample laboratory report image
sample_lab_report.png	Example report image for testing OCR
artifacts/	Stores the trained machine learning model files
API Endpoints
Predict a Disease
POST /predict
This endpoint accepts a list of symptom values and returns the predicted disease and risk percentage.

Example request:

{
  "symptoms": [1, 0, 1, 0, 1]
}
Example response:

{
  "disease": "Example Disease",
  "risk_percentage": 87.45
}
Upload a Laboratory Report
POST /upload-report
This endpoint accepts a laboratory report image and extracts medical test information from it.

Supported file types:

PNG
JPG
JPEG
Example response:

{
  "status": "success",
  "data": {
    "Hemoglobin": "13.5 g/dL",
    "Glucose": "110 mg/dL"
  }
}
Generate an AI Clinical Summary
POST /generate-summary
This endpoint generates an English summary for doctors and an Urdu summary for patients.

Example request:

{
  "symptoms": [
    "fever",
    "headache",
    "body pain"
  ],
  "predicted_disease": "Flu",
  "risk_percentage": 82.5
}
Example response:

{
  "status": "success",
  "data": {
    "doctor_english_summary": "The symptoms are consistent with a possible flu infection.",
    "patient_urdu_summary": "آپ کی علامات فلو سے ملتی جلتی ہیں۔ بہتر تشخیص کے لیے ڈاکٹر سے مشورہ کریں۔"
  }
}
Create a Patient Record
POST /patient-records
This endpoint saves patient information, symptoms, predictions, laboratory results, and clinical summaries in the database.

Get Patient Records
GET /patient-records
This endpoint retrieves saved consultation records.

Optional query parameters:

skip
limit
Example:

GET /patient-records?skip=0&limit=20
Requirements
Before running the project, make sure the following software is installed:

Python 3.9 or newer
PostgreSQL
Git
A Google Gemini API key
A Groq API key