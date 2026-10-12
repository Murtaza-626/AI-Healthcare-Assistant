"""
init_db.py
Explicitly loads all ER diagram models and creates tables in PostgreSQL.
"""
from database import engine, Base
import models  # Must import models so SQLAlchemy registers Doctor, Patient, Consultation, etc.

def init_tables():
    print("Tables found in your Python code:", list(Base.metadata.tables.keys())) 
    print("Connecting to PostgreSQL and creating tables according to ER diagram...")
    # This automatically detects ForeignKeys and builds tables in the correct order:
    # 1. doctors -> 2. patients -> 3. consultations -> 4. lab_reports, predictions
    Base.metadata.create_all(bind=engine)
    print("All tables ('doctors', 'patients', 'consultations', 'lab_reports', 'predictions') created successfully!")

if __name__ == "__main__":
    init_tables()