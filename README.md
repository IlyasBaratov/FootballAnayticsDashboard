# Football Analytics Dashboard

Smart Soccer Analytics Dashboard – A modern, well-architected Python web application with PostgreSQL and Docker that ingests soccer match data and provides interactive visualizations (shot maps, player heat maps, passing networks) plus optional AI models for advanced stats such as expected goals.

## 🎯 Project Overview

This is a **production-ready FastAPI application** following Python best practices with:
- Clean architecture and separation of concerns
- RESTful API design
- Type-safe code with full type hints
- Comprehensive documentation
- Docker support for easy deployment

## ✨ Features

- ⚽ **Comprehensive Football Data Management**
  - Leagues, Seasons, Teams, Players
  - Fixtures, Events, Lineups
  - Player & Team Statistics
  - Standings & Transfers

- 🔌 **RESTful API**
  - Full CRUD operations for all resources
  - Pagination support
  - Advanced filtering
  - Auto-generated interactive documentation

- 🏗️ **Clean Architecture**
  - Layered design (API → Service → Repository → Models)
  - Dependency injection
  - Generic repository pattern
  - Type-safe throughout

- 🐘 **PostgreSQL Database**
  - Comprehensive schema
  - Proper indexing and constraints
  - Connection pooling
  - Transaction management

- 🐳 **Docker Support**
  - Multi-container setup
  - Easy deployment
  - Development & production configs

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- Docker & Docker Compose (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/IlyasBaratov/FootballAnayticsDashboard.git
   cd FootballAnayticsDashboard
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r backEnd/requirements.txt
   ```

4. **Configure environment**
   ```bash
   copy .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the API**
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

### Base URL
`http://localhost:8000/api/v1`

### Available Endpoints

#### System
- `GET /` - Health check
- `GET /health` - Health status
- `GET /api/v1/test-db` - Database connectivity test

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

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

## 🔒 Security

- Environment-based configuration
- SQL injection protection via ORM
- Input validation with Pydantic
- CORS configuration
- Database connection pooling

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

[Your License Here]

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
