"""
Custom exceptions and error handlers for the application.
"""
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette import status


class NotFoundError(Exception):
    """Raised when a resource is not found."""
    
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)


class ConflictError(Exception):
    """Raised when there's a conflict with existing data."""
    
    def __init__(self, message: str = "Resource conflict"):
        self.message = message
        super().__init__(self.message)


class ValidationError(Exception):
    """Raised when validation fails."""
    
    def __init__(self, message: str = "Validation error"):
        self.message = message
        super().__init__(self.message)


async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    """Handler for NotFoundError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message}
    )


async def conflict_handler(request: Request, exc: ConflictError) -> JSONResponse:
    """Handler for ConflictError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.message}
    )


async def validation_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handler for ValidationError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.message}
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for generic exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred"}
    )
