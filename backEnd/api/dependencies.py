from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from backEnd.main import SessionLocal
from backEnd.services.service import *

from backEnd.models.model import League, Team, Fixture, Player
from backEnd.repository.rep import Repository


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