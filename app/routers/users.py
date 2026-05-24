"""Endpoint for users."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.services import user_services
from app.config import settings

router = APIRouter(prefix="/v2/user", tags=["users"])


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str, db: Session = Depends(get_db)):
    """Return a user by ID."""
    user = user_services.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404,
                            detail="User not found in the DataBase")
    return user


@router.get("", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    """Return all users."""
    return user_services.get_all_users(db)


@router.post("", status_code=201, response_model=UserOut)
def create_user(body: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    if user_services.get_user_by_email(db, body.email):
        raise HTTPException(status_code=409,
                            detail="Email already taken")
    user = user_services.create_user(db,
                                     body.email,
                                     body.password,
                                     settings.initial_tokens)
    return user


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: str, body: UserUpdate, db: Session = Depends(get_db)):
    """Update a user's email and/or password."""
    user = user_services.update_user(db, user_id, body.email, body.password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserOut)
def patch_user(user_id: str, body: UserUpdate, db: Session = Depends(get_db)):
    """Partially update a user's email and/or password."""
    user = user_services.update_user(db, user_id, body.email, body.password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    """Delete a user by ID."""
    result = user_services.delete_user(db, user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
