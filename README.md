# Assignment 2 - Olympics API v2

## Group Members
- robinahe@stud.ntnu.no

## Github
https://github.com/Heimdalingen/Olympics-api-v2

## Description
This is the second assignment, built on top of Assignment 1. The idea was to take the Olympics REST API and put it all into Docker containers using Docker Compose. I swapped out SQLite for Postgres and added three extra microservices — a logger, a rate limiter, and a token shop. Redis handles caching and Nginx sits in front of everything as a reverse proxy.

## Architecture

| Container | What it does |
|---|---|
| `nginx` | Reverse proxy on port 80, routes traffic to the main API |
| `main-api` | The main FastAPI application |
| `db` | Postgres — stores both the Olympic dataset and users |
| `cache` | Redis — caches GET responses for 60 seconds |
| `logger` | Writes a log entry for every request to daily CSV files |
| `rate-limiter` | Tracks how many requests a user makes and adds a delay if they go too fast |
| `token-shop` | Lets users buy tokens using one-time codes |

## How to run

```bash
docker compose up --build
```

The database seeds itself on first run (loads all the Olympic data automatically). Once it's ready the API is live at `http://localhost`. First startup takes a bit longer because of the seeding, so just give it a minute.

## Endpoints

### Users
- `POST /v2/user` — Register a new user (starts with 10 tokens)
- `GET /v2/user` — List all users
- `GET /v2/user/{user_id}` — Get a specific user
- `PUT /v2/user/{user_id}` — Update a user
- `PATCH /v2/user/{user_id}` — Partially update a user
- `DELETE /v2/user/{user_id}` — Delete a user

### Tokens
- `POST /v2/tokens` — Add tokens to a user directly (admin use)
- `GET /v2/tokens/price` — Check the current token price
- `POST /v2/tokens/redeem` — Redeem a code from the token shop

### Data endpoints (all cost 1 token per request)
These support JSON, XML and CSV — just set the `Accept` header accordingly.

- `GET /v2/athlete/{athlete_id}?user_id=` — All events for an athlete
- `GET /v2/country/{noc}?user_id=` — All events for a country (e.g. `NOR`, `USA`)
- `GET /v2/sport/{sport}?user_id=` — Events for a sport, optional filters: `country`, `year`, `medal`, `limit`
- `POST /v2/event?user_id=` — Add a new event record

## Token shop

The token shop runs on port 8003. The flow is:

1. Buy a code (you can do this directly in Swagger at `http://localhost:8003/docs`):
```bash
POST http://localhost:8003/buy
{"username": "your@email.com", "money": 5}
# returns {"secret": "<code>"}
```

2. Redeem it through the main API to get the tokens added to your account:
```bash
POST http://localhost/v2/tokens/redeem
{"user_id": "<your-user-id>", "code": "<secret-code>"}
```

Tokens you get = money × price (default is 10 tokens per unit of money). Each code can only be used once.

## Swagger / interactive docs
```
http://localhost/docs        ← main API
http://localhost:8003/docs   ← token shop
```

## A few other things worth knowing

**Caching** — GET requests to the athlete, country and sport endpoints are cached in Redis for 60 seconds. If you hit the same endpoint twice within that window the second response comes straight from cache.

**Rate limiting** — If a user sends 10 or more requests within a 10 second window, a delay kicks in using `f(r) = r/10` seconds. So the more requests you spam, the longer you wait.

**Logging** — Every request gets logged (timestamp, user, endpoint) to a daily CSV file stored in a Docker volume. You can adjust how many days of logs to keep by calling `POST logger:8000/retention` with `{"n": <days>}`.
