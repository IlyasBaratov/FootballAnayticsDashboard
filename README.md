# ⚽ Football Analytics Dashboard

A comprehensive Football Analytics Backend built with FastAPI that integrates with **API-Football v3** to provide real-time football data, statistics, predictions, and analytics.

## 🎯 Project Overview

This is a **production-ready FastAPI application** with complete **API-Football integration** featuring:
- 🔴 **Live match data** with real-time scores
- 📊 **League standings** and rankings
- 📈 **Team & player statistics**
- 🔮 **Match predictions** and analytics
- 🏆 **Top scorers** and assists leaders
- ⚽ **Comprehensive match details** (events, lineups, stats)
- 🎯 **Head-to-head** comparisons
- Clean architecture and separation of concerns
- RESTful API design with auto-generated docs
- Type-safe code with full type hints
- Docker support for easy deployment

## ✨ Key Features

### 🌐 API-Football Integration
- **Live Matches** - Real-time scores and match updates
- **Fixtures & Schedules** - Past and upcoming matches
- **League Standings** - Up-to-date league tables
- **Team Statistics** - Comprehensive performance metrics
- **Player Data** - Top scorers, assists, and player search
- **Match Predictions** - AI-powered outcome forecasts
- **Match Details** - Events, lineups, and detailed statistics
- **Head-to-Head** - Historical matchup analysis

### 🏗️ Technical Features
- ⚡ **Async/Await** - High-performance async operations
- 🔄 **Smart Rate Limiting** - Automatic API rate management
- 💾 **Intelligent Caching** - Optimized response times
- 🔐 **Type Safety** - Full type hints throughout
- 📚 **Auto Documentation** - Swagger UI and ReDoc
- 🐳 **Docker Ready** - Complete containerization
- � **Clean Architecture** - Layered design pattern

### 📊 Data Management
- ⚽ **Comprehensive Football Data**
  - Leagues, Seasons, Teams, Players
  - Fixtures, Events, Lineups
  - Player & Team Statistics
  - Standings & Transfers
- 🐘 **PostgreSQL Database**
  - Normalized schema design
  - Proper indexing and constraints
  - Connection pooling
  - Transaction management

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- API-Football API Key ([Get free key](https://www.api-football.com/))
- Docker & Docker Compose (optional)

### Installation

#### Option 1: Quick Start (5 minutes)

See **[QUICK_START.md](./QUICK_START.md)** for the fastest way to get started!

#### Option 2: Manual Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/IlyasBaratov/FootballAnayticsDashboard.git
   cd FootballAnayticsDashboard
   ```

2. **Get API-Football API Key**
   - Visit [API-Football](https://www.api-football.com/)
   - Sign up for a free account
   - Get your API key from dashboard

3. **Set up Python environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   cd backEnd
   pip install -r requirements.txt
   ```

5. **Configure environment**
   ```bash
   # Copy template
   cp ../.env.example ../.env
   
   # Edit .env and add your API key
   # API_FOOTBALL_KEY=your_actual_api_key_here
   ```

6. **Setup database**
   ```bash
   # Create database
   createdb football_analytics
   
   # Run schema
   psql -d football_analytics -f ../db/db_schema.sql
   ```

7. **Run the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

8. **Access the API**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Using Docker

```bash
docker-compose up -d
```

## 📁 Project Structure

```
FootballAnayticsDashboard/
├── backEnd/
│   ├── core/              # Core functionality
│   │   ├── config.py      # Settings management
│   │   └── database.py    # Database session
│   ├── models/            # SQLAlchemy ORM models
│   │   └── model.py       # All database models
│   ├── schemas/           # Pydantic schemas
│   │   ├── league.py
│   │   ├── team.py
│   │   ├── player.py
│   │   └── fixture.py
│   ├── repository/        # Data access layer
│   │   └── rep.py         # Generic repository
│   ├── services/          # Business logic layer
│   │   └── service.py     # Service classes
│   ├── api/              # API layer
│   │   ├── dependencies.py
│   │   ├── errors.py
│   │   └── routers/       # API endpoints
│   │       ├── leagues.py
│   │       ├── teams.py
│   │       ├── players.py
│   │       └── fixtures.py
│   ├── main.py           # FastAPI app
│   └── requirements.txt   # Dependencies
├── db/                    # Database files
│   ├── db_schema.sql
│   └── example_queries.sql
├── frontEnd/              # Frontend (TODO)
├── docker-compose.yml
├── Dockerfile
├── run.py                 # Quick start script
└── README.md
```

## 📚 API Documentation

### Complete Documentation
- 📖 **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - Complete API reference with examples
- 🚀 **[QUICK_START.md](./QUICK_START.md)** - Get started in 5 minutes
- 📊 **[BACKEND_SUMMARY.md](./BACKEND_SUMMARY.md)** - Architecture and feature overview

### Base URL
`http://localhost:8000/api/v1`

### 🔴 Live & Real-Time Data

#### Matches & Fixtures
- `GET /api/v1/matches/live` - All live matches
- `GET /api/v1/matches/today` - Today's matches
- `GET /api/v1/matches/date/{date}` - Matches by date
- `GET /api/v1/matches/league/{league_id}` - League fixtures
- `GET /api/v1/matches/team/{team_id}` - Team fixtures
- `GET /api/v1/matches/{fixture_id}` - Match details
- `GET /api/v1/matches/{fixture_id}/statistics` - Match stats
- `GET /api/v1/matches/{fixture_id}/events` - Goals, cards, subs
- `GET /api/v1/matches/{fixture_id}/lineups` - Team lineups
- `GET /api/v1/matches/h2h/{team1}/{team2}` - Head-to-head

#### Standings
- `GET /api/v1/standings/{league_id}` - League table/standings

#### Statistics
- `GET /api/v1/statistics/team/{team_id}` - Team statistics
- `GET /api/v1/statistics/top-scorers/{league_id}` - Top scorers
- `GET /api/v1/statistics/top-assists/{league_id}` - Top assists
- `GET /api/v1/statistics/players/search` - Search players

#### Predictions
- `GET /api/v1/predictions/{fixture_id}` - Match predictions

### 📊 Database CRUD Operations

#### Leagues
- `GET /api/v1/leagues` - List leagues
- `GET /api/v1/leagues/{id}` - Get league
- `POST /api/v1/leagues` - Create league
- `PUT /api/v1/leagues/{id}` - Update league
- `DELETE /api/v1/leagues/{id}` - Delete league
- `GET /api/v1/leagues/{id}/seasons` - Get seasons

#### Teams
- `GET /api/v1/teams` - List teams
- `GET /api/v1/teams/{id}` - Get team
- `POST /api/v1/teams` - Create team
- `PUT /api/v1/teams/{id}` - Update team
- `DELETE /api/v1/teams/{id}` - Delete team
- `GET /api/v1/teams/{id}/fixtures` - Get fixtures

#### Players
- `GET /api/v1/players` - List players
- `GET /api/v1/players/{id}` - Get player
- `POST /api/v1/players` - Create player
- `PUT /api/v1/players/{id}` - Update player
- `DELETE /api/v1/players/{id}` - Delete player
- `GET /api/v1/players/{id}/current-team` - Get current team

#### Fixtures
- `GET /api/v1/fixtures` - List fixtures
- `GET /api/v1/fixtures/{id}` - Get fixture
- `GET /api/v1/fixtures/{id}/details` - Get with events/stats
- `POST /api/v1/fixtures` - Create fixture
- `PUT /api/v1/fixtures/{id}` - Update fixture
- `DELETE /api/v1/fixtures/{id}` - Delete fixture

### Interactive Documentation
Visit http://localhost:8000/docs for the interactive Swagger UI where you can test all endpoints.

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type hints
- **PostgreSQL** - Relational database
- **Uvicorn** - ASGI server

### Development Tools
- **Docker** - Containerization
- **Git** - Version control

## ⚙️ Configuration

Environment variables can be set in `.env` file:

```env
# Application
APP_NAME=Football Analytics API
DEBUG=False

# Database
DATABASE_URL=postgresql+psycopg2://user:password@host:port/database

# Database Pool
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10

# CORS
CORS_ORIGINS=*
```

## 🏗️ Architecture

### Layered Architecture

```
API Layer (FastAPI Routes)
    ↓
Service Layer (Business Logic)
    ↓
Repository Layer (Data Access)
    ↓
Models Layer (Database)
```

### Design Patterns
- **Repository Pattern** - Abstract data access
- **Service Pattern** - Business logic encapsulation
- **Dependency Injection** - Loose coupling
- **Factory Pattern** - Service creation

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# With coverage
pytest --cov=backEnd
```

## 📖 Documentation Files

- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick reference guide
- **[REFACTORING_GUIDE.md](REFACTORING_GUIDE.md)** - Complete documentation
- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Migration from old structure
- **[REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)** - What was changed

### Code Style
- Follow PEP 8
- Use type hints
- Write docstrings
- Add tests for new features

## 📝 Development Guidelines

### Adding New Features
1. Create Pydantic schemas in `schemas/`
2. Add business logic in `services/`
3. Create API routes in `api/routers/`
4. Register routes in `api/routers/__init__.py`
5. Write tests

### Best Practices
- ✅ Use type hints everywhere
- ✅ Write comprehensive docstrings
- ✅ Follow single responsibility principle
- ✅ Keep functions small and focused
- ✅ Use dependency injection
- ✅ Handle errors appropriately
- ✅ Write tests


**TODO**: Add authentication & authorization

## 🚧 Roadmap

- [ ] Add authentication/authorization (JWT)
- [ ] Add comprehensive test suite
- [ ] Add caching layer (Redis)
- [ ] Add API rate limiting
- [ ] Add logging and monitoring
- [ ] Add database migrations (Alembic)
- [ ] Add CI/CD pipeline
- [ ] Complete frontend implementation
- [ ] Add WebSocket support for real-time updates
- [ ] Add advanced analytics features

## 📄 License
----
## 👥 Authors

**Ilyas Baratov** - [GitHub](https://github.com/IlyasBaratov)

## 🙏 Acknowledgments

- FastAPI framework and community
- SQLAlchemy ORM
- Pydantic validation library
- Football-Data.org for data APIs

## 📞 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ⚽ and ❤️**
