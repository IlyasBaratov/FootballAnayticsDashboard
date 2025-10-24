"""
Schemas for standings, statistics, and analytics data.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field


# ============ STANDINGS ============

class StandingTeamInfo(BaseModel):
    """Team info in standing."""
    id: int
    name: str
    logo: Optional[str] = None


class StandingStats(BaseModel):
    """Standing statistics."""
    played: int = 0
    win: int = 0
    draw: int = 0
    lose: int = 0
    goals_for: int = Field(default=0, alias="goalsFor")
    goals_against: int = Field(default=0, alias="goalsAgainst")
    
    class Config:
        populate_by_name = True


class StandingEntry(BaseModel):
    """Single standing entry."""
    rank: int
    team: StandingTeamInfo
    points: int
    goalsDiff: int
    group: Optional[str] = None
    form: Optional[str] = None  # e.g., "WWDLW"
    status: Optional[str] = None
    description: Optional[str] = None
    all: StandingStats
    home: StandingStats
    away: StandingStats
    update: Optional[str] = None


class StandingsResponse(BaseModel):
    """League standings response."""
    league: Dict[str, Any]
    standings: List[List[StandingEntry]]


# ============ FIXTURE/MATCH ============

class FixtureStatus(BaseModel):
    """Fixture status info."""
    long: str  # e.g., "Match Finished"
    short: str  # e.g., "FT"
    elapsed: Optional[int] = None  # minutes played


class FixtureVenue(BaseModel):
    """Fixture venue info."""
    id: Optional[int] = None
    name: Optional[str] = None
    city: Optional[str] = None


class FixtureTeam(BaseModel):
    """Team info in fixture."""
    id: int
    name: str
    logo: Optional[str] = None
    winner: Optional[bool] = None


class FixtureScore(BaseModel):
    """Match score."""
    home: Optional[int] = None
    away: Optional[int] = None


class FixtureScores(BaseModel):
    """All match scores."""
    halftime: FixtureScore
    fulltime: FixtureScore
    extratime: Optional[FixtureScore] = None
    penalty: Optional[FixtureScore] = None


class FixtureInfo(BaseModel):
    """Fixture basic info."""
    id: int
    referee: Optional[str] = None
    timezone: str
    date: datetime
    timestamp: int
    venue: FixtureVenue
    status: FixtureStatus


class LeagueInfo(BaseModel):
    """League info in fixture."""
    id: int
    name: str
    country: str
    logo: Optional[str] = None
    flag: Optional[str] = None
    season: int
    round: Optional[str] = None


class FixtureResponse(BaseModel):
    """Complete fixture response."""
    fixture: FixtureInfo
    league: LeagueInfo
    teams: Dict[str, FixtureTeam]  # "home" and "away"
    goals: FixtureScore
    score: FixtureScores


# ============ MATCH STATISTICS ============

class MatchStatistic(BaseModel):
    """Single match statistic."""
    type: str  # e.g., "Shots on Goal", "Possession"
    value: Any  # Can be int, str, or None


class TeamMatchStatistics(BaseModel):
    """Match statistics for one team."""
    team: FixtureTeam
    statistics: List[MatchStatistic]


class MatchStatisticsResponse(BaseModel):
    """Complete match statistics."""
    fixture_id: int
    teams: List[TeamMatchStatistics]


# ============ MATCH EVENTS ============

class EventTime(BaseModel):
    """Event time info."""
    elapsed: int
    extra: Optional[int] = None


class EventPlayer(BaseModel):
    """Player involved in event."""
    id: Optional[int] = None
    name: str


class MatchEvent(BaseModel):
    """Single match event (goal, card, substitution)."""
    time: EventTime
    team: FixtureTeam
    player: EventPlayer
    assist: Optional[EventPlayer] = None
    type: str  # "Goal", "Card", "subst"
    detail: str  # "Normal Goal", "Yellow Card", etc.
    comments: Optional[str] = None


class MatchEventsResponse(BaseModel):
    """Match events response."""
    fixture_id: int
    events: List[MatchEvent]


# ============ LINEUPS ============

class LineupPlayer(BaseModel):
    """Player in lineup."""
    id: int
    name: str
    number: int
    pos: str  # Position
    grid: Optional[str] = None  # Formation position like "4:2:3:1"


class Coach(BaseModel):
    """Coach info."""
    id: Optional[int] = None
    name: str
    photo: Optional[str] = None


class TeamLineup(BaseModel):
    """Team lineup."""
    team: FixtureTeam
    coach: Coach
    formation: str
    startXI: List[Dict[str, LineupPlayer]]
    substitutes: List[Dict[str, LineupPlayer]]


class LineupsResponse(BaseModel):
    """Lineups response."""
    fixture_id: int
    lineups: List[TeamLineup]


# ============ TEAM STATISTICS ============

class TeamSeasonStatistics(BaseModel):
    """Team statistics for a season."""
    team: Dict[str, Any]
    league: Dict[str, Any]
    form: Optional[str] = None
    fixtures: Dict[str, Any]
    goals: Dict[str, Any]
    biggest: Dict[str, Any]
    clean_sheet: Dict[str, Any]
    failed_to_score: Dict[str, Any]
    penalty: Dict[str, Any]
    lineups: List[Dict[str, Any]]
    cards: Dict[str, Any]


# ============ PLAYERS ============

class PlayerInfo(BaseModel):
    """Player basic info."""
    id: int
    name: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    age: Optional[int] = None
    nationality: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    photo: Optional[str] = None


class PlayerStatistics(BaseModel):
    """Player statistics."""
    team: Dict[str, Any]
    league: Dict[str, Any]
    games: Dict[str, Any]
    substitutes: Dict[str, Any]
    shots: Dict[str, Any]
    goals: Dict[str, Any]
    passes: Dict[str, Any]
    tackles: Dict[str, Any]
    duels: Dict[str, Any]
    dribbles: Dict[str, Any]
    fouls: Dict[str, Any]
    cards: Dict[str, Any]
    penalty: Dict[str, Any]


class PlayerResponse(BaseModel):
    """Player response."""
    player: PlayerInfo
    statistics: List[PlayerStatistics]


# ============ TOP SCORERS / ASSISTS ============

class TopPlayerEntry(BaseModel):
    """Top scorer or assist entry."""
    player: PlayerInfo
    statistics: List[PlayerStatistics]


class TopPlayersResponse(BaseModel):
    """Top players response."""
    players: List[TopPlayerEntry]


# ============ PREDICTIONS ============

class PredictionTeam(BaseModel):
    """Team info in prediction."""
    id: int
    name: str
    logo: Optional[str] = None
    last_5: Optional[Dict[str, Any]] = None
    league: Optional[Dict[str, Any]] = None


class PredictionComparison(BaseModel):
    """Comparison data."""
    form: Dict[str, str]
    att: Dict[str, str]
    def_: Dict[str, str] = Field(alias="def")
    poisson_distribution: Dict[str, str]
    h2h: Dict[str, str]
    goals: Dict[str, str]
    total: Dict[str, str]
    
    class Config:
        populate_by_name = True


class PredictionData(BaseModel):
    """Prediction data."""
    predictions: Dict[str, Any]
    league: Dict[str, Any]
    teams: Dict[str, PredictionTeam]
    comparison: Optional[PredictionComparison] = None
    h2h: Optional[List[FixtureResponse]] = None


# ============ HEAD TO HEAD ============

class HeadToHeadResponse(BaseModel):
    """Head to head response."""
    fixtures: List[FixtureResponse]
    total_matches: int


# ============ LIVE FIXTURES ============

class LiveFixturesResponse(BaseModel):
    """Live fixtures response."""
    fixtures: List[FixtureResponse]
    count: int


# ============ SEARCH & FILTER ============

class FixtureFilters(BaseModel):
    """Filters for fixture queries."""
    league_id: Optional[int] = None
    season: Optional[int] = None
    team_id: Optional[int] = None
    date: Optional[date] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    status: Optional[str] = None  # NS, LIVE, FT, etc.
    round: Optional[str] = None


class StandingsFilters(BaseModel):
    """Filters for standings queries."""
    league_id: int
    season: int
    team_id: Optional[int] = None


# ============ DASHBOARD SUMMARY ============

class DashboardSummary(BaseModel):
    """Dashboard summary data."""
    live_matches_count: int
    today_matches_count: int
    featured_leagues: List[Dict[str, Any]]
    top_scorers_preview: List[TopPlayerEntry]
    recent_results: List[FixtureResponse]


# ============ LEAGUE SUMMARY ============

class LeagueSummary(BaseModel):
    """League summary with key info."""
    league_id: int
    league_name: str
    country: str
    logo: Optional[str] = None
    current_season: int
    current_round: Optional[str] = None
    standings_available: bool
    fixtures_count: int
