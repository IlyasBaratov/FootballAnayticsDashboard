"""
Dependency injection for FastAPI endpoints.
"""
from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.model import League, Team, Fixture, Player
from repository.rep import Repository
from services.service import (
    LeagueService, 
    PlayerService, 
    FixtureService, 
    TeamService
)
from controllers.football_controller import FootballController


def get_league_service(db: Session = Depends(get_db)) -> LeagueService:
    """Get league service instance."""
    return LeagueService(repository=Repository(League), db=db)


def get_team_service(db: Session = Depends(get_db)) -> TeamService:
    """Get team service instance."""
    return TeamService(repository=Repository(Team), db=db)


def get_fixture_service(db: Session = Depends(get_db)) -> FixtureService:
    """Get fixture service instance."""
    return FixtureService(repository=Repository(Fixture), db=db)


def get_player_service(db: Session = Depends(get_db)) -> PlayerService:
    """Get player service instance."""
    return PlayerService(repository=Repository(Player), db=db)


def get_football_controller(db: Session = Depends(get_db)) -> FootballController:
    """Get football controller instance for API-Football integration."""
    return FootballController(db=db)

