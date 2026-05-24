"""Router for athlete endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.olympic import OlympicEventOut
from app.services import query_services
from app.utils.dependencies import consume_token
from app.utils.integrations import apply_rate_limit, cache_get, cache_set
from app.utils.responses import format_response

router = APIRouter(prefix="/v2/athlete", tags=["athletes"])


@router.get("/{athlete_id}")
def get_athlete(athlete_id: int, user_id: str, request: Request, db: Session = Depends(get_db), limit: int = 100):
    """Return all Olympic events for a given athlete."""
    consume_token(user_id, db)
    apply_rate_limit(user_id)

    # Check cache before hitting the database
    cache_key = f"athlete:{athlete_id}:{limit}"
    cached = cache_get(cache_key)
    if cached is not None:
        return format_response(cached, request.headers.get("accept", ""))

    # Cache miss — query the database
    events = query_services.get_athlete(db, athlete_id, limit)
    if not events:
        raise HTTPException(status_code=404, detail="Athlete not found")

    # Serialize and store in cache for next time
    serialized = [OlympicEventOut.model_validate(e).model_dump() for e in events]
    cache_set(cache_key, serialized)
    return format_response(serialized, request.headers.get("accept", ""))
