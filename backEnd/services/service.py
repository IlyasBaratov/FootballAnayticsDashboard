"""
Service layer for business logic.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import is_dataclass, asdict
from typing import Optional, TypeVar, Generic, Any, List, Union, Dict

from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from backEnd.repository.rep import Repository
from backEnd.models.model import Team, League, Player, Fixture, Season

M = TypeVar('M')
Incoming = Union[Dict[str, Any], BaseModel, Any]


def convert_to_dict(payload: Incoming) -> Dict[str, Any]:
    """
    Convert various input types to dictionary.
    
    Args:
        payload: Input data (dict, Pydantic model, dataclass, or object)
        
    Returns:
        Dictionary representation of the input
    """
    if isinstance(payload, BaseModel):
        return payload.model_dump(exclude_unset=True)
    if is_dataclass(payload):
        return asdict(payload)
    if isinstance(payload, dict):
        return payload
    # Extract public attributes from object
    return {k: v for k, v in vars(payload).items() if not k.startswith("_")}


class BaseService(Generic[M]):
    """
    Base service class with common CRUD operations.
    
    Type Parameters:
        M: SQLAlchemy model class
    """
    
    def __init__(self, repository: Repository[M], db: Session) -> None:
        self.repository = repository
        self.db = db

    # READ METHODS
    
    def get(self, id: Any) -> Optional[M]:
        """Get a single record by ID."""
        return self.repository.get(self.db, id)

    def list(self, *, limit: int = 100, offset: int = 0) -> List[M]:
        """
        List records with pagination.
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of records
        """
        items = self.repository.all(self.db)
        return items[offset: offset + limit]

    def find(self, **filters: Any) -> List[M]:
        """Find records matching filters."""
        return self.repository.find(self.db, **filters)

    # CREATE METHODS
    
    def create(self, data: Incoming) -> M:
        """
        Create a new record.
        
        Args:
            data: Data for the new record
            
        Returns:
            Created record
        """
        payload = convert_to_dict(data)
        obj = self.repository.model(**payload)
        return self.repository.add(self.db, obj)

    def bulk_create(self, items: Sequence[Incoming]) -> Sequence[M]:
        """
        Create multiple records.
        
        Args:
            items: List of data for new records
            
        Returns:
            List of created records
        """
        objects = []
        for item in items:
            obj_data = convert_to_dict(item)
            obj = self.repository.model(**obj_data)
            objects.append(obj)
        return self.repository.add_many(self.db, objects)

    # UPDATE/UPSERT/DELETE METHODS

    def upsert(self, *, match_fields: Dict[str, Any], defaults: Incoming) -> M:
        """
        Insert or update a record.
        
        Args:
            match_fields: Fields to match for existing record
            defaults: Fields to update/insert
            
        Returns:
            The created or updated record
        """
        return self.repository.upsert(
            self.db, 
            match_fields=match_fields, 
            defaults=convert_to_dict(defaults)
        )

    def update(self, id: Any, data: Incoming) -> Optional[M]:
        """
        Update a record.
        
        Args:
            id: Record ID
            data: Data to update
            
        Returns:
            Updated record or None if not found
        """
        obj = self.repository.get(self.db, id)
        if not obj:
            return None
        payload = convert_to_dict(data)
        for k, v in payload.items():
            setattr(obj, k, v)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: Any) -> Optional[M]:
        """Delete a record by ID."""
        return self.repository.delete(self.db, id)


# DOMAIN-SPECIFIC SERVICES


class TeamService(BaseService[Team]):
    """Service for team-related operations."""
    
    def get_fixtures(self, team_id: int) -> List[Fixture]:
        """
        Get all fixtures for a team.
        
        Args:
            team_id: Team ID
            
        Returns:
            List of fixtures where the team played
        """
        statement = (
            select(Fixture)
            .where(or_(Fixture.home_team_id == team_id, Fixture.away_team_id == team_id))
            .order_by(Fixture.event_date.desc().nullslast())
        )
        return list(self.db.execute(statement).scalars().all())


class LeagueService(BaseService[League]):
    """Service for league-related operations."""
    
    def get_seasons(self, league_id: int) -> List[Season]:
        """
        Get all seasons for a league.
        
        Args:
            league_id: League ID
            
        Returns:
            List of seasons ordered by year (descending)
        """
        statement = (
            select(Season)
            .where(Season.league_id == league_id)
            .order_by(Season.year.desc())
        )
        return list(self.db.execute(statement).scalars().all())


class FixtureService(BaseService[Fixture]):
    """Service for fixture-related operations."""
    
    def with_events(self, fixture_id: int) -> Optional[Fixture]:
        """
        Get fixture with all related data (events, lineups, stats).
        
        Args:
            fixture_id: Fixture ID
            
        Returns:
            Fixture with eagerly loaded relationships or None
        """
        from sqlalchemy.orm import joinedload
        from backEnd.models.model import Event, Lineup, PlayerStat, TeamStat
        
        statement = (
            select(Fixture)
            .options(
                joinedload(Fixture.events),
                joinedload(Fixture.lineups),
                joinedload(Fixture.player_stats),
                joinedload(Fixture.team_stats),
            )
            .where(Fixture.id == fixture_id)
        )
        return self.db.execute(statement).scalars().first()


class PlayerService(BaseService[Player]):
    """Service for player-related operations."""
    
    def get_current_team(self, player_id: int) -> Optional[Team]:
        """
        Get the current team for a player.
        
        Args:
            player_id: Player ID
            
        Returns:
            Current team or None
        """
        from backEnd.models.model import PlayerTeamSeason
        
        statement = (
            select(Team)
            .join(PlayerTeamSeason, PlayerTeamSeason.team_id == Team.id)
            .where(
                PlayerTeamSeason.player_id == player_id,
                PlayerTeamSeason.is_current == True
            )
            .limit(1)
        )
        return self.db.execute(statement).scalars().first()














