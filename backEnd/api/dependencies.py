from typing import Generator
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os
import httpx
from fastapi import Depends
from sqlalchemy.orm import Session, sessionmaker

# from backEnd.main import SessionLocal
from backEnd.services.service import *

from backEnd.models.model import League, Team, Fixture, Player
from backEnd.repository.rep import Repository

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
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db()-> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def getLeagueService(db: Session = Depends(get_db)) -> LeagueService:
    return LeagueService(repository=Repository(League), db=db)
def getTeamService(db: Session = Depends(get_db)) -> TeamService:
    return TeamService(repository=Repository(Team), db=db)
def getFixtureService(db: Session = Depends(get_db)) -> FixtureService:
    return FixtureService(repository=Repository(Fixture), db=db)
def getPlayerService(db: Session = Depends(get_db)) -> PlayerService:
    return PlayerService(repository=Repository(Player), db=db)
async def get_http_client() -> httpx.AsyncClient:
    timeout = httpx.Timeout(15.0)  # seconds
    limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)
    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        yield client