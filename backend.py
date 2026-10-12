from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
import os
import json
import joblib
import numpy as np
import uvicorn
import io
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai
from groq import Groq
import models
from database import engine, get_db 
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing.")
genai.configure(api_key = GEMINI_API_KEY)

app = FastAPI()

ARTIFACTS_DIR = 'artifacts'

try:
    model_pkl = joblib.load(os.path.join(ARTIFACTS_DIR, 'disease_model.pkl'))
    label_encoder = joblib.load(os.path.join(ARTIFACTS_DIR, 'label_encoder.pkl'))
except FileNotFoundError:
    raise RuntimeError("Model files not found")

class SymptomInput(BaseModel):
    symptoms: list[int]

with open(os.path.join(ARTIFACTS_DIR, 'symptom_features.json'), 'r') as f:
    expected_features = json.load(f)


# Predict Disease:
@app.post("/predict")
async def predict_disease(payload: SymptomInput):
    symptoms_list = payload.symptoms

    input_features = np.array([symptoms_list])

    predicted_numeric_idx = model_pkl.predict(input_features)
    predict_disease = label_encoder.inverse_transform(predicted_numeric_idx)[0]

    probabilities = model_pkl.predict_proba(input_features)[0]
    risk_percentage = max(probabilities) * 100

    return {
        "disease": str(predict_disease),
        "risk_percentage": float(round(risk_percentage, 2))
    }



# OCR Part:
@app.post("/upload-report")
async def upload_report(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        model = genai.GenerativeModel('gemini-3.8-flash')
        prompt = "Extract the medical test names and numerical values from this lab report image and return them in JSON format."

        # Calling the API:
        response = model.generate_content([prompt, image])
        clean_text = response.text.strip()

        if clean_text.startswith("```json"):
            clean_text = clean_text.removeprefix("```json").removesuffix("```").strip()

        extracted_data = json.loads(clean_text)

        return {
            "status": "success",
            "data": extracted_data
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="Failed to parse lab report. Ensure the image is clear and well-lit.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")


# Generating Summary:

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is missing. Check your .env file.")

# Initializing the synchronous Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

# Defining the Input Schema
class SummaryRequest(BaseModel):
    symptoms: list[str]
    predicted_disease: str
    risk_percentage: float

class PatientRecordCreate(BaseModel):
    doctor_id: str  # Add this so you know which doctor this patient belongs to
    patient_name: str
    patient_age: Optional[int] = None
    patient_gender: Optional[str] = None
    patient_dob: Optional[str] = None
    symptoms: List[str]
    predicted_disease: str
    risk_percentage: float
    lab_results: Optional[Dict[str, Any]] = None
    clinical_summary: Optional[Dict[str, Any]] = None

# --- NEW ROUTE (PHASE 2, PART 4) ---
@app.post("/generate-summary")
async def generate_summary(payload: SummaryRequest):

    try:
        # 1. Constructing the System Prompt
        # We explicitly command the model to return JSON to prevent parsing errors on the frontend.
        system_prompt = (
            "You are an expert clinical AI assistant. You receive patient symptoms and an ML model prediction. "
            "Your output MUST be a valid JSON object with exactly two keys: "
            "'doctor_english_summary' (a concise 2-sentence clinical reasoning for a physician) and "
            "'patient_urdu_summary' (a simple, empathetic 2-sentence summary written in Urdu script for the patient)."
        )
        
        # 2. Construct the User Prompt with dynamic variables
        user_prompt = (
            f"Symptoms: {', '.join(payload.symptoms)}\n"
            f"Predicted Disease: {payload.predicted_disease}\n"
            f"Risk Probability: {payload.risk_percentage}%"
        )

        # 3. Call the Llama 3.1 8B Instant model via Groq API
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="openai/gpt-oss-20b",
            response_format={"type": "json_object"}, # Forces guaranteed JSON output
            temperature=0.3, # Low temperature for factual, non-creative clinical outputs
        )

        # 4. Parse the generated text back into a Python dictionary
        response_content = json.loads(chat_completion.choices[0].message.content)
        
        return {"status": "success", "data": response_content}

    except Exception as e:
        # Edge Case: Groq API timeout, rate limits, or network failures
        raise HTTPException(status_code=500, detail=f"LLM summary generation failed: {str(e)}")


# 7. Route: Patient Record Database Persistence (Phase 2, Step 5)
# @app.post("/patient-records", status_code=201)
# def create_patient_record(record: PatientRecordCreate, db: Session = Depends(get_db)):
#     """
#     Saves a comprehensive consultation record including symptoms, ML prediction,
#     OCR laboratory metrics, and LLM clinical summaries to PostgreSQL.
#     """
#     try:
#         db_record = models.Patient(
#             doctor_id=record.doctor_id,        # Added: model requires a doctor_id linked to it
#             name=record.patient_name,          # Matches 'name' column
#             date_of_birth= record.patient_dob,      # Matches 'date_of_birth' column
#             gender=record.patient_gender      # Matches 'gender' column
#         )
#         db.add(db_record)
#         db.commit()
#         db.refresh(db_record)
#         return {"status": "success", "record_id": db_record.id, "created_at": db_record.created_at}
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Database insertion failed: {str(e)}")



@app.post("/patient-records", status_code=201)
def create_patient_record(payload: PatientRecordCreate, db: Session = Depends(get_db)):
    """
    Persists patient demographics linked to doctor_id, records the consultation,
    and saves associated predictions and OCR lab outputs per the ER diagram.
    """
    try:
        # Step A: Verify doctor exists to satisfy foreign key constraint
        doctor_exists = db.query(models.Doctor).filter(models.Doctor.id == payload.doctor_id).first()
        if not doctor_exists:
            # Seed default doctor if testing in local development
            doctor_exists = models.Doctor(
                id=payload.doctor_id,
                name="Dr. Default Clinician",
                email=f"doctor_{str(payload.doctor_id)[:8]}@hospital.org",
                password_hash="argon2_hashed_placeholder"
            )
            db.add(doctor_exists)
            db.flush()

        # Step B: Create Patient entity linked to doctor_id
        new_patient = models.Patient(
            doctor_id=payload.doctor_id,
            name=payload.patient_name,
            date_of_birth=payload.patient_dob,  # Guaranteed valid date object
            gender=payload.patient_gender
        )
        db.add(new_patient)
        db.flush()

        # Step C: Create Consultation entity
        new_consultation = models.Consultation(
            patient_id=new_patient.id,
            symptoms=payload.symptoms,
            urdu_audio_transcript=None,
            english_translation=None
        )
        db.add(new_consultation)
        db.flush()

        # Step D: Create Prediction entity
        llm_text = None
        if payload.clinical_summary:
            llm_text = payload.clinical_summary.get("doctor_english_summary")

        new_prediction = models.Prediction(
            consultation_id=new_consultation.id,
            predicted_disease=payload.predicted_disease,
            risk_percentage=payload.risk_percentage,
            llm_clinical_summary=llm_text
        )
        db.add(new_prediction)

        # Step E: Create LabReport entity if OCR data exists
        if payload.lab_results:
            new_lab_report = models.LabReport(
                consultation_id=new_consultation.id,
                report_image_url=None,
                extracted_ocr_data=payload.lab_results
            )
            db.add(new_lab_report)

        db.commit()

        return {
            "status": "success",
            "doctor_id": str(payload.doctor_id),
            "patient_id": str(new_patient.id),
            "consultation_id": str(new_consultation.id)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database insertion failed: {str(e)}")


@app.get("/patient-records")
def get_patient_records(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    
    # Fetches consultation history to populate the Doctor Consultation Dashboard in Phase 3.
    
    records = db.query(models.PatientRecord).order_by(models.PatientRecord.created_at.desc()).offset(skip).limit(limit).all()
    return {"status": "success", "count": len(records), "data": records}
        
if __name__ == "__main__":
    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)
