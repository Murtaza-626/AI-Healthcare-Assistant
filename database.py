# SQLAlchemy connection and session lifecycle management.

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing. Please define it in your .env file.")

# Create the SQLAlchemy engine
# pool_pre_ping checks the connection health before issuing queries
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal class to generate isolated transactional database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative ORM models
Base = declarative_base()

def get_db():
    """
    FastAPI dependency that yields a database session per request
    and ensures the session is closed cleanly upon request completion.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()