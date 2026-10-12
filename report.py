"""
generate_sample_report.py
Generates a clean synthetic lab report image to test the Phase 2 OCR endpoint.
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_lab_report(output_filename: str = "sample_lab_report.png") -> str:
    # 1. Canvas dimensions and high-contrast clinical color palette
    width, height = 900, 1100
    background_color = (255, 255, 255)
    text_color = (20, 20, 20)
    primary_color = (16, 44, 87)
    border_color = (200, 200, 200)

    image = Image.new("RGB", (width, height), color=background_color)
    draw = ImageDraw.Draw(image)

    # 2. Use system default font (portable across all operating systems)
    font = ImageFont.load_default()

    # 3. Header Section (Hospital / Diagnostic Center Metadata)
    draw.rectangle([(30, 30), (870, 110)], outline=primary_color, width=2)
    draw.text((50, 45), "CITY DIAGNOSTIC CLINIC & PATHOLOGY LABS", fill=primary_color, font=font)
    draw.text((50, 65), "Automated Clinical Biochemistry & Hematology Division", fill=text_color, font=font)
    draw.text((50, 85), "Report Status: Verified Final", fill=text_color, font=font)

    # 4. Patient Demographics Block
    draw.rectangle([(30, 125), (870, 205)], outline=border_color, width=1)
    draw.text((50, 135), "Patient Name: Jane Doe", fill=text_color, font=font)
    draw.text((50, 155), "Age / Gender: 34 Y / Female", fill=text_color, font=font)
    draw.text((50, 175), "Referred By : Dr. S. Ahmed (MD)", fill=text_color, font=font)

    draw.text((520, 135), "Sample ID    : LAB-2026-9812", fill=text_color, font=font)
    draw.text((520, 155), "Collected    : 10-Oct-2026 08:30 AM", fill=text_color, font=font)
    draw.text((520, 175), "Reported     : 10-Oct-2026 11:45 AM", fill=text_color, font=font)

    # 5. Tabular Test Results
    draw.rectangle([(30, 220), (870, 250)], fill=(240, 244, 248), outline=border_color)
    draw.text((50, 230), "TEST DESCRIPTION", fill=primary_color, font=font)
    draw.text((360, 230), "MEASURED VALUE", fill=primary_color, font=font)
    draw.text((540, 230), "UNITS", fill=primary_color, font=font)
    draw.text((700, 230), "REFERENCE RANGE", fill=primary_color, font=font)

    lab_records = [
        ("Hemoglobin", "13.5", "g/dL", "12.0 - 15.5"),
        ("RBC Count", "4.6", "mil/mcL", "4.0 - 5.2"),
        ("WBC Count", "7200", "/mcL", "4500 - 11000"),
        ("Platelet Count", "260000", "/mcL", "150000 - 450000"),
        ("Fasting Blood Glucose", "110", "mg/dL", "70 - 99"),
        ("HbA1c", "5.9", "%", "4.0 - 5.6"),
        ("Serum Creatinine", "0.9", "mg/dL", "0.6 - 1.1"),
        ("Blood Urea Nitrogen", "16", "mg/dL", "7 - 20"),
        ("Total Bilirubin", "0.8", "mg/dL", "0.2 - 1.2"),
        ("ALT (SGPT)", "28", "U/L", "7 - 56"),
        ("AST (SGOT)", "24", "U/L", "10 - 40"),
        ("Serum Cholesterol", "195", "mg/dL", "< 200"),
        ("Serum Triglycerides", "145", "mg/dL", "< 150"),
        ("HDL Cholesterol", "52", "mg/dL", "> 50"),
        ("LDL Cholesterol", "114", "mg/dL", "< 100")
    ]

    current_y = 265
    for test, val, unit, ref in lab_records:
        draw.line([(30, current_y - 5), (870, current_y - 5)], fill=(240, 240, 240), width=1)
        draw.text((50, current_y), test, fill=text_color, font=font)
        draw.text((360, current_y), val, fill=text_color, font=font)
        draw.text((540, current_y), unit, fill=text_color, font=font)
        draw.text((700, current_y), ref, fill=text_color, font=font)
        current_y += 35

    # 6. Footer & Validation Seal
    draw.rectangle([(30, height - 120), (870, height - 50)], outline=border_color, width=1)
    draw.text((50, height - 105), "Electronically Verified By: Dr. R. Malik (Consultant Pathologist)", fill=text_color, font=font)
    draw.text((50, height - 85), "Note: This is a synthetic diagnostic document created for model evaluation.", fill=(120, 120, 120), font=font)

    # 7. Save file locally
    image.save(output_filename)
    return os.path.abspath(output_filename)

if __name__ == "__main__":
    path = create_lab_report()
    print(f"Sample lab report generated at: {path}")