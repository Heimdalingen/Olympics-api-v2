# Assignment 1 - Olympics API

## Group Members
- robinahe@stud.ntnu.no

## Render URL
https://olympics-api-9xyt.onrender.com

## API Documentation
Interactive docs available at: https://olympics-api-9xyt.onrender.com/docs

## Description
A REST API for querying Olympic Games data built with FastAPI and SQLite. Users are given tokens on registration and consume one token per API call.

## Endpoints

### Users
- `POST /v1/user` — Create a user
- `GET /v1/user` — List all users
- `GET /v1/user/{user_id}` — Get a user
- `PUT /v1/user/{user_id}` — Update a user
- `PATCH /v1/user/{user_id}` — Partially update a user
- `DELETE /v1/user/{user_id}` — Delete a user

### Tokens
- `POST /v1/tokens` — Add tokens to a user

### Data (supports JSON, XML, CSV via `Accept` header)
- `GET /v1/athlete/{athlete_id}` — Get events for an athlete
- `GET /v1/country/{noc}` — Get events for a country (e.g. `NOR`)
- `GET /v1/sport/{sport}` — Get events for a sport, with optional filters: `country`, `year`, `medal`, `limit`
- `POST /v1/event` — Create a new event

## Running Locally
```bash
pip install -r requirements.txt
python scripts/seed_db.py
uvicorn app.main:app --reload
```

## Testing
```bash
pytest tests/
```
