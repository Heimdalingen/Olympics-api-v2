"""Router for events endpoint."""
from fastapi import APIRouter, Depends
from app.schemas.olympic import OlympicEventCreate
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import query_services
from app.utils.dependencies import consume_token


router = APIRouter(prefix="/v2/event", tags=["events"])


@router.post("")
def create_events(body: OlympicEventCreate,
                  user_id: str,
                  db: Session = Depends(get_db)):
    """Create a new Olympic event record."""
    consume_token(user_id, db)
    event = query_services.create_event(db, body)
    return event
