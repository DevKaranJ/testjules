from fastapi import HTTPException
from structlog import get_logger

logger = get_logger()


class StrategyNotFoundError(HTTPException):
    def __init__(self, name: str):
        super().__init__(status_code=404, detail=f"Strategy '{name}' not found")


class DatabaseError(HTTPException):
    def __init__(self, detail: str = "Internal database error"):
        super().__init__(status_code=500, detail=detail)


class RateLimitError(HTTPException):
    def __init__(self):
        super().__init__(status_code=429, detail="Rate limit exceeded")


async def log_exception_handler(request, exc):
    logger.error("unhandled_exception", path=str(request.url), exc_info=exc)
    return HTTPException(status_code=500, detail="Internal server error")
