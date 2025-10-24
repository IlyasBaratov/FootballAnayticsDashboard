# Migration Guide - From Old to New Structure

## What Changed?

### 1. **Project Structure** ✅
- Added `core/` package for configuration and database management
- Added `schemas/` package for Pydantic models
- Added `api/routers/` for organized endpoints
- Proper `__init__.py` files in all packages

### 2. **Configuration Management** ✅
- **Old**: Hardcoded configuration scattered across files
- **New**: Centralized in `core/config.py` using `pydantic-settings`
- Environment variables loaded from `.env` file

### 3. **Database Management** ✅
- **Old**: Multiple `SessionLocal` definitions, circular imports
- **New**: Single source of truth in `core/database.py`
- Proper session management with automatic rollback

### 4. **Models** ✅
- **Old**: Base class defined in model file
- **New**: Base imported from `core/database.py`
- No changes to actual model definitions

### 5. **Repository Pattern** ✅
- **Old**: Inconsistent naming (`addMany`, `Model`)
- **New**: Pythonic naming (`add_many`, `model`)
- Better type hints and documentation
- Fixed bugs (e.g., `self.db.get` → `db.get`)

### 6. **Services** ✅
- **Old**: Inconsistent method names (`getFixtures`, `converToDict`)
- **New**: PEP 8 compliant names (`get_fixtures`, `convert_to_dict`)
- Better error handling
- Comprehensive documentation

### 7. **API Layer** ✅
- **Old**: Empty router files, no endpoints
- **New**: Full CRUD endpoints for:
  - Leagues
  - Teams
  - Players
  - Fixtures
- Proper HTTP status codes
- Consistent response schemas

### 8. **Error Handling** ✅
- **Old**: Basic exception classes
- **New**: Custom exceptions with proper handlers
- Consistent error responses across all endpoints

### 9. **Dependencies** ✅
- **Old**: Minimal dependencies, database setup in dependencies file
- **New**: Complete set of production-ready dependencies
- Added `pydantic-settings`, `uvicorn`, `python-dotenv`

## How to Migrate

### Step 1: Install New Dependencies

```powershell
cd backEnd
pip install -r requirements.txt
```

### Step 2: Set Up Environment

```powershell
# Copy example env file
Copy-Item ..\.env.example .env

# Edit .env with your settings
notepad .env
```

### Step 3: Update Imports in Your Code

If you have any existing scripts or code that imports from the old structure:

**Old imports:**
```python
from api.dependencies import getLeagueService
from models.model import Team
from services.service import BaseService
```

**New imports:**
```python
from backEnd.api.dependencies import get_league_service
from backEnd.models.model import Team
from backEnd.services.service import BaseService
```

### Step 4: Test the Application

```powershell
# Run the server
uvicorn backEnd.main:app --reload

# Test the endpoints
# Open browser: http://localhost:8000/docs
```

### Step 5: Clean Up Old Files (Optional)

The following files are now obsolete:
- `backEnd/repository/engine.py` (replaced by `core/database.py`)
- `backEnd/controllers/controller.py` (empty, not used)

You can delete them:
```powershell
Remove-Item backEnd\repository\engine.py
Remove-Item backEnd\controllers\controller.py
```

## Key Improvements

### 1. Type Safety
All functions now have proper type hints:
```python
def get(self, db: Session, id: Any) -> Optional[M]:
    """Get a single record by ID."""
    return db.get(self.model, id)
```

### 2. Dependency Injection
Clean, testable dependencies:
```python
@router.get("/{league_id}")
def get_league(
    league_id: int,
    service: LeagueService = Depends(get_league_service)
):
    return service.get(league_id)
```

### 3. Consistent API Design
All endpoints follow REST conventions:
- `GET /api/v1/teams` - List
- `GET /api/v1/teams/{id}` - Detail
- `POST /api/v1/teams` - Create
- `PUT /api/v1/teams/{id}` - Update
- `DELETE /api/v1/teams/{id}` - Delete

### 4. Proper Error Handling
```python
league = service.get(league_id)
if not league:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"League with ID {league_id} not found"
    )
return league
```

### 5. Documentation
- Every function has docstrings
- Auto-generated API docs at `/docs`
- Clear code organization

## Testing Your Changes

### 1. Test Database Connection
```powershell
curl http://localhost:8000/api/v1/test-db
```

### 2. Test Endpoints
```powershell
# Get all teams
curl http://localhost:8000/api/v1/teams

# Get specific team
curl http://localhost:8000/api/v1/teams/1

# Create a team (example)
curl -X POST http://localhost:8000/api/v1/teams `
  -H "Content-Type: application/json" `
  -d '{"id": 1, "name": "Test Team"}'
```

### 3. Check Interactive Docs
Open in browser: http://localhost:8000/docs

## Troubleshooting

### Issue: Module Import Errors
**Solution**: Make sure you're running from the project root and using proper absolute imports.

### Issue: Database Connection Failed
**Solution**: Check your `.env` file and ensure DATABASE_URL is correct.

### Issue: Missing Dependencies
**Solution**: Run `pip install -r backEnd/requirements.txt` again.

## Next Steps

1. ✅ Basic CRUD operations working
2. 🔄 Add authentication/authorization
3. 🔄 Add pagination helpers
4. 🔄 Add filtering and sorting
5. 🔄 Add comprehensive tests
6. 🔄 Add API rate limiting
7. 🔄 Add caching layer
8. 🔄 Add logging middleware

## Questions?

The refactored code is now:
- ✅ More maintainable
- ✅ Better documented
- ✅ Type-safe
- ✅ Following Python best practices
- ✅ Production-ready

Enjoy your clean codebase! 🎉
