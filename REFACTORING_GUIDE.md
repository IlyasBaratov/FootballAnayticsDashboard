# Football Analytics Dashboard - Refactored

A modern, well-structured FastAPI application for football analytics with a clean architecture following Python best practices.

## 🏗️ Project Structure

```
backEnd/
├── core/               # Core functionality (config, database)
│   ├── __init__.py
│   ├── config.py      # Application settings
│   └── database.py    # Database connection and session management
├── models/            # SQLAlchemy ORM models
│   ├── __init__.py
│   └── model.py       # All database models
├── schemas/           # Pydantic schemas for validation
│   ├── __init__.py
│   ├── base.py
│   ├── league.py
│   ├── team.py
│   ├── player.py
│   └── fixture.py
├── repository/        # Data access layer
│   ├── __init__.py
│   └── rep.py         # Generic repository pattern
├── services/          # Business logic layer
│   ├── __init__.py
│   └── service.py     # Service classes
├── api/               # API layer
│   ├── __init__.py
│   ├── dependencies.py # Dependency injection
│   ├── errors.py      # Error handlers
│   └── routers/       # API endpoints
│       ├── __init__.py
│       ├── leagues.py
│       ├── teams.py
│       ├── players.py
│       └── fixtures.py
├── main.py            # Application entry point
└── requirements.txt   # Python dependencies
```

## ✨ Key Features

### Clean Architecture
- **Separation of Concerns**: Clear boundaries between layers (API, Service, Repository, Models)
- **Dependency Injection**: Using FastAPI's dependency system
- **Generic Repository Pattern**: Reusable CRUD operations
- **Service Layer**: Business logic isolated from API endpoints

### Best Practices Implemented

1. **Configuration Management**
   - Environment-based configuration using `pydantic-settings`
   - Cached settings with `@lru_cache`
   - Type-safe configuration

2. **Database Management**
   - Proper session handling with context managers
   - Connection pooling with configurable parameters
   - Automatic rollback on errors

3. **API Design**
   - RESTful endpoints with proper HTTP methods
   - Consistent response schemas using Pydantic
   - Proper status codes (200, 201, 204, 404, etc.)
   - Comprehensive error handling

4. **Type Safety**
   - Full type hints throughout the codebase
   - Pydantic models for request/response validation
   - Generic types for reusable components

5. **Documentation**
   - Docstrings for all classes and functions
   - Auto-generated API docs (Swagger/ReDoc)
   - Clear code comments

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- Docker (optional)

### Installation

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
   pip install -r backEnd/requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   uvicorn backEnd.main:app --reload
   ```

### Using Docker

```bash
docker-compose up -d
```

## 📚 API Endpoints

### Base URL
- Development: `http://localhost:8000`
- API Prefix: `/api/v1`

### Available Endpoints

#### Health & Status
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/v1/test-db` - Database connectivity test

#### Leagues
- `GET /api/v1/leagues` - List all leagues
- `GET /api/v1/leagues/{id}` - Get specific league
- `POST /api/v1/leagues` - Create league
- `PUT /api/v1/leagues/{id}` - Update league
- `DELETE /api/v1/leagues/{id}` - Delete league
- `GET /api/v1/leagues/{id}/seasons` - Get league seasons

#### Teams
- `GET /api/v1/teams` - List all teams
- `GET /api/v1/teams/{id}` - Get specific team
- `POST /api/v1/teams` - Create team
- `PUT /api/v1/teams/{id}` - Update team
- `DELETE /api/v1/teams/{id}` - Delete team
- `GET /api/v1/teams/{id}/fixtures` - Get team fixtures

#### Players
- `GET /api/v1/players` - List all players
- `GET /api/v1/players/{id}` - Get specific player
- `POST /api/v1/players` - Create player
- `PUT /api/v1/players/{id}` - Update player
- `DELETE /api/v1/players/{id}` - Delete player
- `GET /api/v1/players/{id}/current-team` - Get player's current team

#### Fixtures
- `GET /api/v1/fixtures` - List all fixtures
- `GET /api/v1/fixtures/{id}` - Get specific fixture
- `GET /api/v1/fixtures/{id}/details` - Get fixture with events and stats
- `POST /api/v1/fixtures` - Create fixture
- `PUT /api/v1/fixtures/{id}` - Update fixture
- `DELETE /api/v1/fixtures/{id}` - Delete fixture

### Interactive API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

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

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## 📝 Development Guidelines

### Adding a New Endpoint

1. **Create Schema** (in `schemas/`)
   ```python
   class ResourceCreate(BaseModel):
       name: str
   
   class ResourceResponse(BaseModel):
       id: int
       name: str
   ```

2. **Create Router** (in `api/routers/`)
   ```python
   @router.get("/", response_model=List[ResourceResponse])
   def list_resources(service: ResourceService = Depends(get_resource_service)):
       return service.list()
   ```

3. **Register Router** (in `api/routers/__init__.py`)
   ```python
   api_router.include_router(resources.router, prefix="/resources", tags=["resources"])
   ```

### Code Style
- Follow PEP 8
- Use type hints
- Write docstrings
- Keep functions small and focused
- Use meaningful variable names

## 🔒 Security Considerations

- Use environment variables for sensitive data
- Implement authentication/authorization (TODO)
- Validate all input data with Pydantic
- Use parameterized queries (SQLAlchemy ORM)
- Enable CORS selectively in production

## 📈 Performance Tips

- Use database connection pooling
- Implement caching where appropriate
- Use `joinedload` for eager loading relationships
- Paginate large result sets
- Monitor database query performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## 📄 License

MIT License

## 👥 Authors

[Your Name/Team]

## 🙏 Acknowledgments

- FastAPI framework
- SQLAlchemy ORM
- Pydantic validation
