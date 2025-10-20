# backEnd/main.py
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Retrieve the PostgreSQL connection string
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Initialize FastAPI app
app = FastAPI(title="Football Analytics API")


# Dependency for database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Football Analytics API connected successfully!"}


# Test database connection
@app.get("/test_db")
def test_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1;")).fetchone()
        return {"db_connection": "ok" if result else "failed"}
    except Exception as e:
        return {"db_connection": "error", "details": str(e)}
