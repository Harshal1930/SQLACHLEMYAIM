# main.py (or where you're working)
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import os
from utils.utils_root import env_get  # Ensure the module path is correct
from sqlalchemy.ext.declarative import declarative_base



DATABASE_URL = env_get("DB_URL")

# Set up SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for getting a session
def getdb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
