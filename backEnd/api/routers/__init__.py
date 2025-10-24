"""API routers package."""
from fastapi import APIRouter

from backEnd.api.routers import (
    leagues, 
    teams, 
    players, 
    fixtures,
    matches,
    standings,
    statistics,
    predictions
)

api_router = APIRouter()

# Database CRUD routers
api_router.include_router(leagues.router, prefix="/leagues", tags=["leagues"])
api_router.include_router(teams.router, prefix="/teams", tags=["teams"])
api_router.include_router(players.router, prefix="/players", tags=["players"])
api_router.include_router(fixtures.router, prefix="/fixtures", tags=["fixtures"])

# API-Football integration routers
api_router.include_router(matches.router, prefix="/matches", tags=["matches"])
api_router.include_router(standings.router, prefix="/standings", tags=["standings"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["statistics"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"])

__all__ = ["api_router"]
