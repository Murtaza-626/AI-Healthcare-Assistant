# AI Healthcare Assistant

An AI-powered healthcare application that predicts possible diseases from patient symptoms, extracts information from laboratory reports, generates clinical summaries in English and Urdu, and stores patient consultation records.

**Note:** This project is developed for educational and research purposes. It is not a substitute for professional medical diagnosis or advice.

## Features

### 1. Disease Prediction

* Predicts possible diseases based on patient symptoms.
* Returns a prediction percentage.
* Uses a trained XGBoost classification model.

### 2. Laboratory Report Analysis

* Accepts laboratory report images in PNG, JPG, and JPEG formats.
* Uses Google Gemini API to extract test names, values, and units.
* Returns extracted information as structured data.

### 3. AI Clinical Summaries

* Uses Groq API to generate clinical summaries.
* Provides an English summary for doctors.
* Provides a simple Urdu explanation for patients.

### 4. Patient Record Management

* Stores doctor and patient information.
* Saves consultation details, symptoms, predictions, laboratory results, and clinical summaries.
* Retrieves previously saved patient records.

## Technology Stack

| Category         | Technologies                                 |
| ---------------- | -------------------------------------------- |
| Backend          | Python, FastAPI, Uvicorn, Pydantic           |
| Machine Learning | XGBoost, Scikit-learn, NumPy, Pandas, Joblib |
| AI Services      | Google Gemini API, Groq API                  |
| Database         | PostgreSQL, SQLAlchemy, JSONB                |
| Image Processing | Pillow                                       |

## Project Structure (Implemented Yet)

```text
AI-Healthcare-Assistant/
├── artifacts/
│   ├── disease_model.pkl
│   ├── label_encoder.pkl
│   └── symptom_features.json
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
```

### Main Files

| File                   | Description                                          |
| ---------------------- | ---------------------------------------------------- |
| `backend.py`           | FastAPI application and API endpoints                |
| `database.py`          | Database connection and session management           |
| `models.py`            | SQLAlchemy database models                           |
| `init_db.py`           | Database table initialization                        |
| `model_training.py`    | Trains and saves the disease prediction model        |
| `model_training.ipynb` | Notebook for model training                          |
| `report.py`            | Generates a sample laboratory report                 |
| `artifacts/`           | Stores trained model files and symptom configuration |

## API Endpoints

### 1. Predict a Disease

**`POST /predict`**

Predicts a possible disease from symptom values.

Example request:

```json
{
  "symptoms": [1, 0, 1, 0, 1]
}
```

Example response:

```json
{
  "disease": "Example Disease",
  "risk_percentage": 87.45
}
```

### 2. Upload a Laboratory Report

**`POST /upload-report`**

Uploads a laboratory report image and extracts medical test information.

Supported formats: PNG, JPG, JPEG.

Example response:

```json
{
  "status": "success",
  "data": {
    "Hemoglobin": "13.5 g/dL",
    "Glucose": "110 mg/dL"
  }
}
```

### 3. Generate Clinical Summaries

**`POST /generate-summary`**

Generates English and Urdu summaries from patient symptoms and prediction information.

Example request:

```json
{
  "symptoms": ["fever", "headache", "body pain"],
  "predicted_disease": "Flu",
  "risk_percentage": 82.5
}
```

### 4. Create a Patient Record

**`POST /patient-records`**

Saves patient information, symptoms, consultation details, predictions, laboratory results, and clinical summaries.

### 5. Retrieve Patient Records

**`GET /patient-records`**

Retrieves saved patient consultation records.

Optional query parameters:

* `skip`: Number of records to skip.
* `limit`: Maximum number of records to return.

Example:

```http
GET /patient-records?skip=0&limit=20
```

## Requirements

* Python 3.13.5 or newer
* PostgreSQL
* Git
* Google Gemini API key
* Groq API key

## Setup and Usage

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install the required dependencies.
4. Configure PostgreSQL and the required environment variables.
5. Initialize the database tables.
6. Start the FastAPI server.

Run the application:

```bash
python backend.py
```

Open the interactive API documentation at:

`http://127.0.0.1:8000/docs`

## Disclaimer

Disease predictions and AI-generated summaries are for educational and research purposes only. They must not be treated as confirmed diagnoses or used as a substitute for professional medical judgment.
