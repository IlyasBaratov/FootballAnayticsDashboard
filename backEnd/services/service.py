from __future__ import annotations

from collections.abc import Sequence
from dataclasses import is_dataclass, asdict
from typing import Optional, TypeVar, Generic, Any, List, Union, Dict
from pydantic.v1 import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.testing import exclude

from backEnd.models.model import League
from backEnd.repository.rep import Repository

M = TypeVar('M')
Incoming = Union[Dict[str, Any], BaseModel, Any]

def converToDict(payload: Incoming) -> Dict[str: Any]:
    if isinstance(payload, BaseModel):
        return payload.model_dump(exclude_unset = True)
    if is_dataclass(payload):
        return asdict(payload)
    if isinstance(payload, dict):
        return payload

    #  I have no clue how this on works, but it does!!!
    return {k: v for k, v in vars(payload).items() if not k.startswith("_")}

class BaseService(Generic[M]):
    def __init__(self, repository: Repository[M], db: Session) -> None:
        self.repository = repository
        self.db = db

    """
    READ METHODS
    """
    def get(self) -> Optional[M]:
        return self.repository.get(self.db, id)

    def list(self, *, limit: int  = 100, offset: int = 0) -> List[M]:
        items = self.repository.all(self.db)
        return items[offset: offset + limit]

    def find(self, **filters: Any) -> List[M]:
        return self.repository.find(self.db, **filters)

    '''
    CREATE METHODS
    '''
    def create(self, data: Incoming) -> M:
        payload = converToDict(data)
        object = self.repository.Model(**payload)
        return self.repository.add(self.db, object)
    def bulkCreate(self, items: Sequence[Incoming]) -> Sequence[M]:
        object = []
        for item in items:
            obj_data = converToDict(item)
            obj = self.repo.Model(**obj_data)
            object.append(obj)
        created_objects = self.repo.addMany(self.db, object)
        return created_objects

    """
    UPDATE/UPSERT/DELETE METHODS
    """

    def upsert(self, *, matchFields: Dict[str, Any], defaults: Incoming) -> M:
        return self.repository.upsert(self.db, matchFields = matchFields, defaults = converToDict(defaults))

    def update(self, id:Any, data: Incoming) -> Optional[M]:
        object = self.repository.get(self.db, id)
        if not object:
            return None
        payload = converToDict(data)

        # I have no clue how it works but it works
        for k, v in payload.items():
            setattr(object, k, v)
        self.db.commit()
        self.db.refresh(object)
        return object

    def delete(self, id: Any) -> Optional[M]:
        return self.repo.delete(self.db, id)


    """
    DOMAIN SERVICES!!!
    """
from backEnd.models.model import *

class TeamService(BaseService[Team]):
    def getFixtures(self, teamId: int) -> List[Fixture]:
        from sqlalchemy import select, or_
        from backEnd.models.model import Fixture as Fx
        statement = (
            select(Fx)
            .where(or_(Fx.home_team_id == teamId, Fx.away_team_id == teamId))
            .order_by(Fx.event_date.desc().nullslast())
        )
        return list (self.db.execute(statement).scalars().all())
class LeagueService(BaseService[League]):
    def getSeasons(self, leagueId: int) -> List[Any]:
        from sqlalchemy import select, or_
        from backEnd.models.model import Season
        statement = select(Season).where(Season.league_id == leagueId).order_by(Season.year.desc())
        return list (self.db.execute(statement).scalars().all())
class FixtureService(BaseService[Fixture]):
    def withEvents(self, fixtureId: int) -> Optional[Fixture]:
        from sqlalchemy import select, or_
        from backEnd.models.model import Event, Lineup, PlayerStat, TeamStat;
        from sqlalchemy.orm import joinedload
        statement = (
            select(Fixture)
            .options(
                joinedload(Fixture.events),
                joinedload(Fixture.lineups),
                joinedload(Fixture.player_stats),
                joinedload(Fixture.team_stats),
            )
            .where(Fixture.id == fixtureId)
        )
        return self.db.execute(statement).scalars().first()
class PlayerService(BaseService[Player]):
    def getCurrentTeam(self, playerId: int) -> Optional[Team]:
        from sqlalchemy import select, or_
        from backEnd.models.model import Team, PlayerTeamSeason
        statement = (
            select(Team)
            .join(PlayerTeamSeason, PlayerTeamSeason.team_id == Team.id)
            .where(PlayerTeamSeason.player_id == playerId, PlayerTeamSeason.is_current == True)
            .limit(1)
        )
        return self.db.execute(statement).scalars().first()













