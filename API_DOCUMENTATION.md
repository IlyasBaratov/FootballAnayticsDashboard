# Football Analytics Backend - API Documentation

## Overview

A comprehensive Football Analytics Backend built with FastAPI that integrates with [API-Football v3](https://www.api-football.com/documentation-v3) to provide real-time football data, statistics, and analytics.

## Features

✅ **Live Match Data** - Real-time scores and match updates
✅ **League Standings** - Up-to-date league tables
✅ **Team Statistics** - Comprehensive team performance metrics
✅ **Player Statistics** - Top scorers, assists, and player search
✅ **Match Predictions** - AI-powered match outcome predictions
✅ **Head-to-Head** - Historical matchup data
✅ **Fixtures & Results** - Past and upcoming matches
✅ **Rate Limiting** - Smart API rate limit management
✅ **Caching** - Optimized response times

## Architecture

```
backEnd/
├── api/
│   ├── routers/          # API endpoints
│   │   ├── matches.py    # Live matches, fixtures
│   │   ├── standings.py  # League standings
│   │   ├── statistics.py # Team & player stats
│   │   ├── predictions.py # Match predictions
│   │   ├── leagues.py    # CRUD for leagues
│   │   ├── teams.py      # CRUD for teams
│   │   ├── players.py    # CRUD for players
│   │   └── fixtures.py   # CRUD for fixtures
│   ├── dependencies.py   # Dependency injection
│   ├── errors.py         # Error handlers
│   └── security.py       # Security utilities
├── controllers/
│   └── football_controller.py  # API-Football integration
├── services/
│   ├── api_football_client.py  # External API client
│   └── service.py              # Business logic layer
├── models/
│   └── model.py          # SQLAlchemy ORM models
├── schemas/
│   ├── analytics.py      # Response schemas
│   ├── league.py         # League schemas
│   ├── team.py           # Team schemas
│   ├── player.py         # Player schemas
│   └── fixture.py        # Fixture schemas
├── repository/
│   └── rep.py            # Database repository
└── core/
    ├── config.py         # Configuration
    └── database.py       # Database connection
```

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL 12+
- API-Football API Key ([Get one here](https://www.api-football.com/))

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd FootballAnayticsDashboard
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
cd backEnd
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp ../.env.example ../.env
# Edit .env and add your API_FOOTBALL_KEY
```

5. **Setup database**
```bash
# Create database
createdb football_analytics

# Run migrations (if using Alembic)
alembic upgrade head

# Or run SQL schema directly
psql -d football_analytics -f ../db/db_schema.sql
```

6. **Run the application**
```bash
# From backEnd directory
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication
Currently no authentication required. Add JWT/API key authentication as needed.

---

## 🎯 Live & Fixtures

### Get Live Matches
```http
GET /api/v1/matches/live
```

**Response:**
```json
{
  "count": 5,
  "fixtures": [...]
}
```

### Get Today's Matches
```http
GET /api/v1/matches/today
```

### Get Matches by Date
```http
GET /api/v1/matches/date/{YYYY-MM-DD}
```

**Example:**
```bash
curl http://localhost:8000/api/v1/matches/date/2024-10-24
```

### Get League Fixtures
```http
GET /api/v1/matches/league/{league_id}?season=2023&round=Regular Season - 10
```

**Parameters:**
- `league_id` (required): League ID
- `season` (required): Season year
- `from_date` (optional): Start date (YYYY-MM-DD)
- `to_date` (optional): End date (YYYY-MM-DD)
- `round` (optional): Specific round

### Get Team Fixtures
```http
GET /api/v1/matches/team/{team_id}?season=2023&last=5
```

**Parameters:**
- `team_id` (required): Team ID
- `season` (optional): Season year
- `last` (optional): Last N fixtures
- `next` (optional): Next N fixtures

### Get Fixture Details
```http
GET /api/v1/matches/{fixture_id}?include_statistics=true&include_events=true&include_lineups=true
```

**Parameters:**
- `include_statistics`: Include match stats
- `include_events`: Include goals, cards, subs
- `include_lineups`: Include team lineups

### Get Match Statistics
```http
GET /api/v1/matches/{fixture_id}/statistics
```

### Get Match Events
```http
GET /api/v1/matches/{fixture_id}/events
```

### Get Match Lineups
```http
GET /api/v1/matches/{fixture_id}/lineups
```

### Head-to-Head
```http
GET /api/v1/matches/h2h/{team1_id}/{team2_id}?last=10
```

---

## 📊 Standings

### Get League Standings
```http
GET /api/v1/standings/{league_id}?season=2023
```

**Example:**
```bash
# Premier League 2023 standings
curl http://localhost:8000/api/v1/standings/39?season=2023
```

**Response:**
```json
{
  "league_id": 39,
  "season": 2023,
  "standings": [[
    {
      "rank": 1,
      "team": {
        "id": 50,
        "name": "Manchester City",
        "logo": "..."
      },
      "points": 89,
      "goalsDiff": 61,
      "all": {
        "played": 38,
        "win": 28,
        "draw": 5,
        "lose": 5,
        "goalsFor": 96,
        "goalsAgainst": 35
      }
    }
  ]]
}
```

---

## 📈 Statistics

### Get Team Statistics
```http
GET /api/v1/statistics/team/{team_id}?league_id=39&season=2023
```

**Response includes:**
- Fixtures played/won/lost
- Goals scored/conceded
- Clean sheets
- Failed to score
- Biggest wins/losses
- Most used formations
- Cards statistics

### Top Scorers
```http
GET /api/v1/statistics/top-scorers/{league_id}?season=2023
```

**Example:**
```bash
# Premier League top scorers 2023
curl http://localhost:8000/api/v1/statistics/top-scorers/39?season=2023
```

### Top Assists
```http
GET /api/v1/statistics/top-assists/{league_id}?season=2023
```

### Search Players
```http
GET /api/v1/statistics/players/search?query=Messi&league_id=140&season=2023
```

**Parameters:**
- `query` (required): Player name (min 2 characters)
- `league_id` (optional): Filter by league
- `season` (optional): Filter by season

---

## 🔮 Predictions

### Get Match Predictions
```http
GET /api/v1/predictions/{fixture_id}
```

**Response includes:**
- Win probability for each team
- Goals predictions
- Form comparison
- Head-to-head history
- Betting advice
- Comparison metrics (attack, defense, form)

---

## 🏆 Leagues (CRUD)

### List All Leagues
```http
GET /api/v1/leagues?limit=100&offset=0
```

### Get League by ID
```http
GET /api/v1/leagues/{league_id}
```

### Create League
```http
POST /api/v1/leagues
Content-Type: application/json

{
  "name": "Premier League",
  "country": "England",
  "type": "League"
}
```

### Update League
```http
PUT /api/v1/leagues/{league_id}
```

### Delete League
```http
DELETE /api/v1/leagues/{league_id}
```

---

## 👥 Teams (CRUD)

Similar CRUD endpoints available for teams:
- `GET /api/v1/teams`
- `GET /api/v1/teams/{team_id}`
- `POST /api/v1/teams`
- `PUT /api/v1/teams/{team_id}`
- `DELETE /api/v1/teams/{team_id}`

---

## ⚽ Players (CRUD)

Similar CRUD endpoints available for players:
- `GET /api/v1/players`
- `GET /api/v1/players/{player_id}`
- `POST /api/v1/players`
- `PUT /api/v1/players/{player_id}`
- `DELETE /api/v1/players/{player_id}`

---

## 🎮 Fixtures (CRUD)

Similar CRUD endpoints available for fixtures:
- `GET /api/v1/fixtures`
- `GET /api/v1/fixtures/{fixture_id}`
- `POST /api/v1/fixtures`
- `PUT /api/v1/fixtures/{fixture_id}`
- `DELETE /api/v1/fixtures/{fixture_id}`

---

## Popular League IDs

| League | ID | Country |
|--------|-------|---------|
| Premier League | 39 | England |
| La Liga | 140 | Spain |
| Bundesliga | 78 | Germany |
| Serie A | 135 | Italy |
| Ligue 1 | 61 | France |
| Champions League | 2 | Europe |
| Europa League | 3 | Europe |
| World Cup | 1 | International |

[Full list of leagues](https://www.api-football.com/documentation-v3#tag/Leagues)

---

## Rate Limiting

The API-Football free tier provides:
- **100 requests/day**
- **10 requests/minute**

The client automatically handles rate limiting with:
- Request queuing
- Exponential backoff retry
- Rate limit warnings in logs

**Tip:** Cache responses aggressively to minimize API calls.

---

## Error Handling

### Error Response Format
```json
{
  "detail": "Error message",
  "status_code": 500
}
```

### Common Status Codes
- `200` - Success
- `404` - Resource not found
- `429` - Rate limit exceeded
- `500` - Internal server error

---

## Development

### Run Tests
```bash
pytest
```

### Code Quality
```bash
# Format code
black .

# Lint
flake8

# Type checking
mypy .
```

### API Documentation
Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

---

## Docker Deployment

```bash
# Build and run with docker-compose
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop services
docker-compose down
```

---

## Environment Variables

See `.env.example` for all configuration options.

**Required:**
- `API_FOOTBALL_KEY` - Your API-Football API key
- `DATABASE_URL` - PostgreSQL connection string

**Optional:**
- `API_FOOTBALL_RATE_LIMIT` - Requests per minute (default: 10)
- `CACHE_TTL_SECONDS` - Cache duration (default: 300)

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## License

[Add your license here]

---

## Support

For issues or questions:
- GitHub Issues: [Your repo URL]
- API-Football Documentation: https://www.api-football.com/documentation-v3
- FastAPI Documentation: https://fastapi.tiangolo.com/

---

## Roadmap

- [ ] WebSocket support for live score updates
- [ ] Redis caching layer
- [ ] User authentication & authorization
- [ ] Favorites & personalization
- [ ] Email notifications
- [ ] GraphQL API
- [ ] Mobile app integration
- [ ] Advanced analytics dashboards
