from fastapi import HTTPException, FastAPI
from starlette import status
class NotFoundError(Exception):
    pass
class ConflictError(Exception):
    pass

def register_error_handlers(app: FastAPI):
    @app.exception_handler(NotFoundError)
    async def not_found_handler(_, exc: NotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    @app.exception_handler(ConflictError)
    async def conflict_handler(_, exc: ConflictError):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))