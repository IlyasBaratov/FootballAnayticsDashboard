"""
SQLAlchemy ORM models for Football Analytics application.
"""
from __future__ import annotations

from typing import List, Optional
import uuid

from sqlalchemy import (
    String, Text, Boolean, Integer, BigInteger, Date, DateTime, Numeric,
    UniqueConstraint, ForeignKey, Index, text, func
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backEnd.core.database import Base


# ---------- 1. Reference tables ----------
class League(Base):
    __tablename__ = "leagues"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # API-Football league id
    name: Mapped[str] = mapped_column(Text, nullable=False)
    country: Mapped[Optional[str]] = mapped_column(Text)
    country_code: Mapped[Optional[str]] = mapped_column(String(8))
    logo: Mapped[Optional[str]] = mapped_column(Text)
    flag: Mapped[Optional[str]] = mapped_column(Text)
    type: Mapped[Optional[str]] = mapped_column(String(64))
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    seasons: Mapped[List["Season"]] = relationship("Season", back_populates="league", cascade="all, delete-orphan")
    fixtures: Mapped[List["Fixture"]] = relationship("Fixture", back_populates="league")


class Season(Base):
    __tablename__ = "seasons"
    __table_args__ = (
        UniqueConstraint("league_id", "year", name="uq_seasons_league_year"),
        Index("idx_seasons_league_year", "league_id", "year"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )
    league_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("leagues.id", ondelete="CASCADE"), nullable=False
    )
    year: Mapped[str] = mapped_column(String(20), nullable=False)
    start_date: Mapped[Optional[Date]] = mapped_column(Date)
    end_date: Mapped[Optional[Date]] = mapped_column(Date)
    coverage: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    league: Mapped["League"] = relationship("League", back_populates="seasons")
    rounds: Mapped[List["Round"]] = relationship("Round", back_populates="season", cascade="all, delete-orphan")
    groups: Mapped[List["Group"]] = relationship("Group", back_populates="season", cascade="all, delete-orphan")
    fixtures: Mapped[List["Fixture"]] = relationship("Fixture", back_populates="season")
    player_team_seasons: Mapped[List["PlayerTeamSeason"]] = relationship("PlayerTeamSeason", back_populates="season")
    team_group_memberships: Mapped[List["TeamGroupMembership"]] = relationship("TeamGroupMembership", back_populates="season")
    standings: Mapped[List["Standing"]] = relationship("Standing", back_populates="season")


class Round(Base):
    __tablename__ = "rounds"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    season_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    round_order: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    season: Mapped["Season"] = relationship("Season", back_populates="rounds")
    fixtures: Mapped[List["Fixture"]] = relationship("Fixture", back_populates="round")


class Group(Base):
    __tablename__ = "groups"
    __table_args__ = (
        UniqueConstraint("season_id", "name", name="uq_groups_season_name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    season_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    season: Mapped["Season"] = relationship("Season", back_populates="groups")
    fixtures: Mapped[List["Fixture"]] = relationship("Fixture", back_populates="group")
    team_memberships: Mapped[List["TeamGroupMembership"]] = relationship("TeamGroupMembership", back_populates="group")
    standings: Mapped[List["Standing"]] = relationship("Standing", back_populates="group")


# ---------- 2. Venues, Teams, Coaches ----------
class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(Text)
    city: Mapped[Optional[str]] = mapped_column(Text)
    capacity: Mapped[Optional[int]] = mapped_column(Integer)
    surface: Mapped[Optional[str]] = mapped_column(Text)
    address: Mapped[Optional[str]] = mapped_column(Text)
    country: Mapped[Optional[str]] = mapped_column(Text)
    latitude: Mapped[Optional[Numeric]] = mapped_column(Numeric(9, 6))
    longitude: Mapped[Optional[Numeric]] = mapped_column(Numeric(9, 6))
    country_code: Mapped[Optional[str]] = mapped_column(String(8))
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    teams: Mapped[List["Team"]] = relationship("Team", back_populates="venue")
    fixtures: Mapped[List["Fixture"]] = relationship("Fixture", back_populates="venue")


class Team(Base):
    __tablename__ = "teams"
    __table_args__ = (UniqueConstraint("name", name="uq_teams_name"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # API-Football team id
    name: Mapped[str] = mapped_column(Text, nullable=False)
    short_code: Mapped[Optional[str]] = mapped_column(String(16))
    country: Mapped[Optional[str]] = mapped_column(Text)
    founded: Mapped[Optional[int]] = mapped_column(Integer)
    national: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"))
    logo: Mapped[Optional[str]] = mapped_column(Text)
    venue_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("venues.id", ondelete="SET NULL"))
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    venue: Mapped[Optional["Venue"]] = relationship("Venue", back_populates="teams")
    coaches: Mapped[List["Coach"]] = relationship("Coach", back_populates="team")
    home_fixtures: Mapped[List["Fixture"]] = relationship("Fixture", back_populates="home_team", foreign_keys="Fixture.home_team_id")
    away_fixtures: Mapped[List["Fixture"]] = relationship("Fixture", back_populates="away_team", foreign_keys="Fixture.away_team_id")

    fixture_teams: Mapped[List["FixtureTeam"]] = relationship("FixtureTeam", back_populates="team", cascade="all, delete-orphan")
    player_team_seasons: Mapped[List["PlayerTeamSeason"]] = relationship("PlayerTeamSeason", back_populates="team")
    transfers_from: Mapped[List["Transfer"]] = relationship("Transfer", back_populates="from_team", foreign_keys="Transfer.from_team_id")
    transfers_to: Mapped[List["Transfer"]] = relationship("Transfer", back_populates="to_team", foreign_keys="Transfer.to_team_id")
    standings: Mapped[List["Standing"]] = relationship("Standing", back_populates="team")
    group_memberships: Mapped[List["TeamGroupMembership"]] = relationship("TeamGroupMembership", back_populates="team")


class Coach(Base):
    __tablename__ = "coaches"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    team_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("teams.id", ondelete="CASCADE"))
    firstname: Mapped[Optional[str]] = mapped_column(Text)
    lastname: Mapped[Optional[str]] = mapped_column(Text)
    name: Mapped[Optional[str]] = mapped_column(Text)
    nationality: Mapped[Optional[str]] = mapped_column(Text)
    birth_date: Mapped[Optional[Date]] = mapped_column(Date)
    birth_place: Mapped[Optional[str]] = mapped_column(Text)
    photo: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    team: Mapped[Optional["Team"]] = relationship("Team", back_populates="coaches")
    lineups: Mapped[List["Lineup"]] = relationship("Lineup", back_populates="coach")


# ---------- 3. Players & roster-by-season ----------
class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    firstname: Mapped[Optional[str]] = mapped_column(Text)
    lastname: Mapped[Optional[str]] = mapped_column(Text)
    name: Mapped[Optional[str]] = mapped_column(Text)
    nationality: Mapped[Optional[str]] = mapped_column(Text)
    birth_date: Mapped[Optional[Date]] = mapped_column(Date)
    birth_place: Mapped[Optional[str]] = mapped_column(Text)
    height: Mapped[Optional[str]] = mapped_column(String(16))
    weight: Mapped[Optional[str]] = mapped_column(String(16))
    photo: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    seasons: Mapped[List["PlayerTeamSeason"]] = relationship("PlayerTeamSeason", back_populates="player")
    events: Mapped[List["Event"]] = relationship("Event", back_populates="player", foreign_keys="Event.player_id")
    assists: Mapped[List["Event"]] = relationship("Event", back_populates="assist", foreign_keys="Event.assist_id")
    stats: Mapped[List["PlayerStat"]] = relationship("PlayerStat", back_populates="player")
    transfers: Mapped[List["Transfer"]] = relationship("Transfer", back_populates="player")


class PlayerTeamSeason(Base):
    __tablename__ = "player_team_seasons"
    __table_args__ = (UniqueConstraint("player_id", "team_id", "season_id", name="uq_pts_player_team_season"),)

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    player_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    team_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    season_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False)
    number: Mapped[Optional[int]] = mapped_column(Integer)
    position: Mapped[Optional[str]] = mapped_column(String(32))
    start_date: Mapped[Optional[Date]] = mapped_column(Date)
    end_date: Mapped[Optional[Date]] = mapped_column(Date)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"))
    contract_info: Mapped[Optional[dict]] = mapped_column(JSONB)

    player: Mapped["Player"] = relationship("Player", back_populates="seasons")
    team: Mapped["Team"] = relationship("Team", back_populates="player_team_seasons")
    season: Mapped["Season"] = relationship("Season", back_populates="player_team_seasons")


# ---------- 4. Fixtures ----------
class Fixture(Base):
    __tablename__ = "fixtures"
    __table_args__ = (
        UniqueConstraint("league_id", "season_id", "id", name="uq_fixtures_league_season_id"),
        Index("idx_fixtures_event_date", "event_date"),
        Index("idx_fixtures_league_season", "league_id", "season_id"),
        Index("idx_fixtures_team_event_date", "home_team_id", "away_team_id", "event_date"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # API fixture id
    league_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("leagues.id", ondelete="SET NULL"))
    season_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("seasons.id", ondelete="SET NULL"))
    round_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("rounds.id", ondelete="SET NULL"))
    group_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("groups.id", ondelete="SET NULL"))
    venue_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("venues.id", ondelete="SET NULL"))
    referee: Mapped[Optional[str]] = mapped_column(Text)
    event_date: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    status: Mapped[Optional[str]] = mapped_column(String(32))
    status_code: Mapped[Optional[int]] = mapped_column(Integer)
    timestamp_utc: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    venue_info: Mapped[Optional[dict]] = mapped_column(JSONB)
    referee_info: Mapped[Optional[dict]] = mapped_column(JSONB)
    home_team_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    away_team_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    home_score: Mapped[Optional[int]] = mapped_column(Integer)
    away_score: Mapped[Optional[int]] = mapped_column(Integer)
    winner: Mapped[Optional[int]] = mapped_column(Integer)  # 1 home, 2 away, 0 draw
    round_name: Mapped[Optional[str]] = mapped_column(Text)
    attendance: Mapped[Optional[int]] = mapped_column(Integer)
    weather: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    league: Mapped[Optional["League"]] = relationship("League", back_populates="fixtures")
    season: Mapped[Optional["Season"]] = relationship("Season", back_populates="fixtures")
    round: Mapped[Optional["Round"]] = relationship("Round", back_populates="fixtures")
    group: Mapped[Optional["Group"]] = relationship("Group", back_populates="fixtures")
    venue: Mapped[Optional["Venue"]] = relationship("Venue", back_populates="fixtures")
    home_team: Mapped["Team"] = relationship("Team", foreign_keys=[home_team_id], back_populates="home_fixtures")
    away_team: Mapped["Team"] = relationship("Team", foreign_keys=[away_team_id], back_populates="away_fixtures")

    fixture_teams: Mapped[List["FixtureTeam"]] = relationship("FixtureTeam", back_populates="fixture", cascade="all, delete-orphan")
    events: Mapped[List["Event"]] = relationship("Event", back_populates="fixture", cascade="all, delete-orphan")
    lineups: Mapped[List["Lineup"]] = relationship("Lineup", back_populates="fixture", cascade="all, delete-orphan")
    player_stats: Mapped[List["PlayerStat"]] = relationship("PlayerStat", back_populates="fixture", cascade="all, delete-orphan")
    team_stats: Mapped[List["TeamStat"]] = relationship("TeamStat", back_populates="fixture", cascade="all, delete-orphan")


class FixtureTeam(Base):
    __tablename__ = "fixture_teams"
    __table_args__ = (
        # Composite PK
        {'postgresql_partition_by': None},
    )

    fixture_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("fixtures.id", ondelete="CASCADE"), primary_key=True
    )
    team_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True
    )
    is_home: Mapped[bool] = mapped_column(Boolean, nullable=False)
    role: Mapped[Optional[str]] = mapped_column(String(32))

    fixture: Mapped["Fixture"] = relationship("Fixture", back_populates="fixture_teams")
    team: Mapped["Team"] = relationship("Team", back_populates="fixture_teams")


# ---------- 5. Events ----------
class Event(Base):
    __tablename__ = "events"
    __table_args__ = (Index("idx_events_fixture_minute", "fixture_id", "minute"),)

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    fixture_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("fixtures.id", ondelete="CASCADE"), nullable=False)
    team_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("teams.id", ondelete="SET NULL"))
    player_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("players.id", ondelete="SET NULL"))
    assist_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("players.id", ondelete="SET NULL"))
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    detail: Mapped[Optional[str]] = mapped_column(Text)
    minute: Mapped[Optional[int]] = mapped_column(Integer)
    extra_minute: Mapped[Optional[int]] = mapped_column(Integer)
    score: Mapped[Optional[str]] = mapped_column(Text)
    position: Mapped[Optional[str]] = mapped_column(String(32))
    outcome: Mapped[Optional[str]] = mapped_column(String(32))
    stats: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    fixture: Mapped["Fixture"] = relationship("Fixture", back_populates="events")
    team: Mapped[Optional["Team"]] = relationship("Team")
    player: Mapped[Optional["Player"]] = relationship("Player", foreign_keys=[player_id], back_populates="events")
    assist: Mapped[Optional["Player"]] = relationship("Player", foreign_keys=[assist_id], back_populates="assists")


# ---------- 6. Lineups ----------
class Lineup(Base):
    __tablename__ = "lineups"
    __table_args__ = (UniqueConstraint("fixture_id", "team_id", name="uq_lineups_fixture_team"),)

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    fixture_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("fixtures.id", ondelete="CASCADE"), nullable=False)
    team_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    coach_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("coaches.id", ondelete="SET NULL"))
    formation: Mapped[Optional[str]] = mapped_column(String(32))
    lineup: Mapped[Optional[dict]] = mapped_column(JSONB)
    bench: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    fixture: Mapped["Fixture"] = relationship("Fixture", back_populates="lineups")
    team: Mapped["Team"] = relationship("Team")
    coach: Mapped[Optional["Coach"]] = relationship("Coach", back_populates="lineups")


# ---------- 7. Statistics ----------
class PlayerStat(Base):
    __tablename__ = "player_stats"
    __table_args__ = (UniqueConstraint("fixture_id", "player_id", name="uq_player_stats_fixture_player"),
                      Index("idx_player_stats_fixture_player", "fixture_id", "player_id"))

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    fixture_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("fixtures.id", ondelete="CASCADE"), nullable=False)
    player_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    team_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    minutes_played: Mapped[Optional[int]] = mapped_column(Integer)
    rating: Mapped[Optional[Numeric]] = mapped_column(Numeric(4, 2))
    shots: Mapped[Optional[dict]] = mapped_column(JSONB)
    passes: Mapped[Optional[dict]] = mapped_column(JSONB)
    tackles: Mapped[Optional[dict]] = mapped_column(JSONB)
    cards: Mapped[Optional[dict]] = mapped_column(JSONB)
    shots_total: Mapped[Optional[int]] = mapped_column(Integer)
    shots_on_goal: Mapped[Optional[int]] = mapped_column(Integer)
    goals: Mapped[Optional[int]] = mapped_column(Integer)
    assists: Mapped[Optional[int]] = mapped_column(Integer)
    substitutions: Mapped[Optional[dict]] = mapped_column(JSONB)
    stats_raw: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    fixture: Mapped["Fixture"] = relationship("Fixture", back_populates="player_stats")
    player: Mapped["Player"] = relationship("Player", back_populates="stats")
    team: Mapped["Team"] = relationship("Team")


class TeamStat(Base):
    __tablename__ = "team_stats"
    __table_args__ = (UniqueConstraint("fixture_id", "team_id", name="uq_team_stats_fixture_team"),
                      Index("idx_team_stats_fixture_team", "fixture_id", "team_id"))

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    fixture_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("fixtures.id", ondelete="CASCADE"), nullable=False)
    team_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    possession: Mapped[Optional[Numeric]] = mapped_column(Numeric(5, 2))
    shots_total: Mapped[Optional[int]] = mapped_column(Integer)
    shots_on_goal: Mapped[Optional[int]] = mapped_column(Integer)
    fouls: Mapped[Optional[int]] = mapped_column(Integer)
    corners: Mapped[Optional[int]] = mapped_column(Integer)
    offsides: Mapped[Optional[int]] = mapped_column(Integer)
    lineup_snapshot: Mapped[Optional[dict]] = mapped_column(JSONB)
    stats_raw: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    fixture: Mapped["Fixture"] = relationship("Fixture", back_populates="team_stats")
    team: Mapped["Team"] = relationship("Team")


# ---------- 8. Standings ----------
class Standing(Base):
    __tablename__ = "standings"
    __table_args__ = (
        UniqueConstraint("league_id", "season_id", "group_id", "team_id", name="uq_standings_league_season_group_team"),
        Index("idx_standings_league_season_rank", "league_id", "season_id", "rank"),
    )

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    league_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("leagues.id", ondelete="CASCADE"))
    season_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("seasons.id", ondelete="CASCADE"))
    group_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"))
    team_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)

    rank: Mapped[Optional[int]] = mapped_column(Integer)
    played: Mapped[int] = mapped_column(Integer, default=0, server_default=text("0"))
    wins: Mapped[int] = mapped_column(Integer, default=0, server_default=text("0"))
    draws: Mapped[int] = mapped_column(Integer, default=0, server_default=text("0"))
    losses: Mapped[int] = mapped_column(Integer, default=0, server_default=text("0"))
    points: Mapped[int] = mapped_column(Integer, default=0, server_default=text("0"))
    goals_for: Mapped[int] = mapped_column(Integer, default=0, server_default=text("0"))
    goals_against: Mapped[int] = mapped_column(Integer, default=0, server_default=text("0"))
    # goal_diff is GENERATED ALWAYS in SQL; not persisted here—read-only column
    goal_diff: Mapped[Optional[int]] = mapped_column(Integer)  # will reflect DB computed column
    form: Mapped[Optional[str]] = mapped_column(Text)
    details: Mapped[Optional[dict]] = mapped_column(JSONB)
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    league: Mapped[Optional["League"]] = relationship("League")
    season: Mapped[Optional["Season"]] = relationship("Season", back_populates="standings")
    group: Mapped[Optional["Group"]] = relationship("Group", back_populates="standings")
    team: Mapped["Team"] = relationship("Team", back_populates="standings")


# ---------- 9. Transfers ----------
class Transfer(Base):
    __tablename__ = "transfers"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    player_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    from_team_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("teams.id", ondelete="SET NULL"))
    to_team_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("teams.id", ondelete="SET NULL"))
    transfer_date: Mapped[Optional[Date]] = mapped_column(Date)
    type: Mapped[Optional[str]] = mapped_column(String(32))
    fee: Mapped[Optional[Numeric]] = mapped_column(Numeric(12, 2))
    details: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    player: Mapped["Player"] = relationship("Player", back_populates="transfers")
    from_team: Mapped[Optional["Team"]] = relationship("Team", foreign_keys=[from_team_id], back_populates="transfers_from")
    to_team: Mapped[Optional["Team"]] = relationship("Team", foreign_keys=[to_team_id], back_populates="transfers_to")


# ---------- 10. News ----------
class News(Base):
    __tablename__ = "news"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    external_id: Mapped[Optional[str]] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    content: Mapped[Optional[str]] = mapped_column(Text)
    source: Mapped[Optional[str]] = mapped_column(Text)
    url: Mapped[Optional[str]] = mapped_column(Text)
    published_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    metadatas: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())


# ---------- 11. Team/Group memberships ----------
class TeamGroupMembership(Base):
    __tablename__ = "team_group_memberships"
    __table_args__ = (UniqueConstraint("team_id", "group_id", "season_id", name="uq_tgm_team_group_season"),)

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    team_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    group_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    season_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False)

    team: Mapped["Team"] = relationship("Team", back_populates="group_memberships")
    group: Mapped["Group"] = relationship("Group", back_populates="team_memberships")
    season: Mapped["Season"] = relationship("Season", back_populates="team_group_memberships")


# ---------- 12. Raw payloads ----------
class RawPayload(Base):
    __tablename__ = "raw_payloads"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    source: Mapped[str] = mapped_column(Text, nullable=False)
    external_id: Mapped[Optional[str]] = mapped_column(Text)
    received_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    payload: Mapped[Optional[dict]] = mapped_column(JSONB)
