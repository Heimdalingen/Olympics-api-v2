"""Schemas for user configuration"""
from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    email: str
    password: str


class UserUpdate(BaseModel):
    """Schema for updating a user's email and/or password."""

    email: Optional[str] = None
    password: Optional[str] = None


class UserOut(BaseModel):
    """Schema for returning user data."""

    id: str
    email: str
    tokens: int

    class Config:
        from_attributes = True


class TokenAdd(BaseModel):
    """Schema for adding tokens to a user."""

    user_id: str
    amount: int
