import time
from collections import defaultdict

from fastapi import FastAPI

app = FastAPI(title="Rate Limiter Service")

# How far back (in seconds) we look when counting requests
WINDOW = 10
# Number of requests within the window before delay kicks in
THRESHOLD = 10

# Stores a list of request timestamps per user_id
request_times: dict[str, list[float]] = defaultdict(list)


@app.post("/{user_id}")
def add_request(user_id: str):
    """Register a new request for the given user."""
    request_times[user_id].append(time.time())
    return {"status": "recorded"}


@app.get("/{user_id}")
def get_delay(user_id: str):
    """Return delay in seconds based on how many requests the user has made in the last 10s.
    
    Uses f(r) = r/10 when r >= 10, otherwise returns 0.
    """
    now = time.time()
    cutoff = now - WINDOW
    # Remove timestamps older than the window
    request_times[user_id] = [t for t in request_times[user_id] if t > cutoff]
    r = len(request_times[user_id])
    delay = r / 10 if r >= THRESHOLD else 0.0
    return {"delay": delay}
