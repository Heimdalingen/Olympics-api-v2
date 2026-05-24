"""FastAPI application entry point."""
import httpx
from fastapi import FastAPI, Request

from app.config import settings
from app.database import Base, engine
from app.routers import athletes, countries, events, sports, tokens, users

app = FastAPI(title="Olympics API v2")
app.include_router(users.router)
app.include_router(tokens.router)
app.include_router(sports.router)
app.include_router(events.router)
app.include_router(countries.router)
app.include_router(athletes.router)

Base.metadata.create_all(bind=engine)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log every incoming request to the logger microservice."""
    response = await call_next(request)
    user_id = request.query_params.get("user_id", "anonymous")
    endpoint = f"{request.method} {request.url.path}"
    try:
        async with httpx.AsyncClient(timeout=1.0) as client:
            await client.post(
                f"{settings.logger_url}/log",
                json={"username": user_id, "endpoint": endpoint},
            )
    except Exception:
        # Don't fail the request if logger is unavailable
        pass
    return response


@app.get("/")
def root():
    """Health check endpoint."""
    return {"message": "Olympics API v2 is running"}
