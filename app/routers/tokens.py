"""Endpoints for token management and token-shop integration."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

import httpx

from app.config import settings
from app.database import get_db
from app.schemas.user import TokenAdd, UserOut
from app.services import token_services

router = APIRouter(prefix="/v2/tokens", tags=["tokens"])


class RedeemCode(BaseModel):
    user_id: str
    code: str


@router.post("", response_model=UserOut)
def add_tokens(body: TokenAdd, db: Session = Depends(get_db)):
    """Add tokens directly to a user (admin use)."""
    result = token_services.add_tokens(db, body.user_id, body.amount)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.post("/redeem", response_model=UserOut)
def redeem_tokens(body: RedeemCode, db: Session = Depends(get_db)):
    """Redeem a token-shop code and add the tokens to the user's account."""
    try:
        with httpx.Client(timeout=5.0) as client:
            resp = client.post(
                f"{settings.token_shop_url}/redeem",
                json={"code": body.code},
            )
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Code not found")
        if resp.status_code == 400:
            raise HTTPException(status_code=400, detail="Code already used")
        resp.raise_for_status()
        tokens_to_add = resp.json()["tokens"]
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Token shop unavailable") from exc

    result = token_services.add_tokens(db, body.user_id, tokens_to_add)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.get("/price")
def get_token_price():
    """Return the current token price from the token shop."""
    try:
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{settings.token_shop_url}/price")
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Token shop unavailable") from exc
