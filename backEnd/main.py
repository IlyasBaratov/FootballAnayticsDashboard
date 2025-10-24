"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from backEnd.core.config import get_settings
from backEnd.core.database import get_db
from backEnd.api.routers import api_router
from backEnd.api.errors import (
    NotFoundError,
    ConflictError,
    ValidationError,
    not_found_handler,
    conflict_handler,
    validation_handler,
    generic_exception_handler
)

settings = get_settings()

# Initialize FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    debug=settings.debug,
    description="RESTful API for Football Analytics Dashboard",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

# Register exception handlers
app.add_exception_handler(NotFoundError, not_found_handler)
app.add_exception_handler(ConflictError, conflict_handler)
app.add_exception_handler(ValidationError, validation_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include API routers
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    """Root endpoint - health check."""
    return {
        "message": "Football Analytics API is running!",
        "version": settings.version,
        "status": "healthy"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/api/v1/test-db")
def test_db(db: Session = Depends(get_db)):
    """Test database connectivity."""
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        return {
            "status": "ok" if result and result[0] == 1 else "failed",
            "message": "Database connection is working"
        }
    except Exception as e:
        return {
            "status": "failed",
            "message": f"Database connection failed: {str(e)}"
        }

