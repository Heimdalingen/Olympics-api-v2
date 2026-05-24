"""Helpers for calling the rate-limiter and cache microservices."""
import json
import time

import httpx
import redis

from app.config import settings

# Single Redis client instance shared across requests
_redis: redis.Redis | None = None


def get_redis() -> redis.Redis:
    """Return a cached Redis client, creating it on first call."""
    global _redis
    if _redis is None:
        _redis = redis.from_url(settings.redis_url, decode_responses=True)
    return _redis

# Rate Limiter section

def apply_rate_limit(user_id: str) -> None:
    """Register a request for user_id and sleep if the rate limit triggers."""
    try:
        with httpx.Client(timeout=2.0) as client:
            # Register the request
            client.post(f"{settings.rate_limiter_url}/{user_id}")
            # Get the delay
            resp = client.get(f"{settings.rate_limiter_url}/{user_id}")
            delay = resp.json().get("delay", 0.0)
        if delay > 0:
            time.sleep(delay)
    except Exception:
        # Don't break the API if rate-limiter is unavailable
        pass

# Cache Section

def cache_get(key: str) -> list | None:
    """Return cached data from Redis, or None on miss."""
    try:
        raw = get_redis().get(key)
        return json.loads(raw) if raw else None
    except Exception:
        return None


def cache_set(key: str, data: list, ttl: int = 60) -> None:
    """Store data in Redis with a 60 second expiry by default."""
    try:
        get_redis().setex(key, ttl, json.dumps(data))
    except Exception:
        pass