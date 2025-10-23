# backEnd/main.py
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os

# Do NOT rely on load_dotenv inside containers; compose injects env vars.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@db:5432/football_analytics"
)

if not DATABASE_URL:
    # Extra guard; logs help if something is wrong
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(title="Football Analytics API")

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@app.get("/")
def root():
    return {"message": "Football Analytics API connected successfully!"}

@app.get("/test_db")
def test_db(db: Session = Depends(get_db)):
    row = db.execute(text("SELECT 1")).fetchone()
    return {"db_connection": "ok" if row and row[0] == 1 else "failed"}
