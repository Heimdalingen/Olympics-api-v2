# Assignment 2 - Olympics API v2

## Group Members
- robinahe@stud.ntnu.no

## Github
https://github.com/Heimdalingen/Olympics-api-v2

## Description
Builds on Assignment 1. The Olympics REST API is now fully containerised using Docker Compose. SQLite has been replaced with Postgres, and three new microservices have been added: a logger, a rate limiter, and a token shop. Redis is used as a cache layer. All traffic goes through Nginx as a reverse proxy.

## Architecture

| Container | Purpose |
|---|---|
| `nginx` | Reverse proxy / versioning server (port 80) |
| `main-api` | Olympics FastAPI application |
| `db` | Postgres database (Olympic data + users) |
| `cache` | Redis — caches GET responses for 60 seconds |
| `logger` | Logs all requests to daily CSV files |
| `rate-limiter` | Tracks per-user request rate, adds delay when exceeded |
| `token-shop` | Handles token purchases via one-time secret codes |

## Running

```bash
docker compose up --build
```

The database is seeded automatically on first run. API is available at `http://localhost`.

## Endpoints

### Users
- `POST /v2/user` — Create a user (receives 10 tokens on registration)
- `GET /v2/user` — List all users
- `GET /v2/user/{user_id}` — Get a user
- `PUT /v2/user/{user_id}` — Update a user
- `PATCH /v2/user/{user_id}` — Partially update a user
- `DELETE /v2/user/{user_id}` — Delete a user

### Tokens
- `POST /v2/tokens` — Add tokens directly to a user (admin)
- `GET /v2/tokens/price` — Get current token price from the token shop
- `POST /v2/tokens/redeem` — Redeem a token shop code to add tokens

### Data (supports JSON, XML, CSV via `Accept` header)
- `GET /v2/athlete/{athlete_id}?user_id=` — Get events for an athlete
- `GET /v2/country/{noc}?user_id=` — Get events for a country (e.g. `NOR`)
- `GET /v2/sport/{sport}?user_id=` — Get events for a sport, optional filters: `country`, `year`, `medal`, `limit`
- `POST /v2/event` — Create a new event

## Token Shop Flow

1. Buy a code directly from the token shop:
```bash
POST http://localhost:8003/buy
{"username": "your@email.com", "money": 5}
```
Returns `{"secret": "<code>"}`.

2. Redeem the code through the main API to add tokens to your account:
```bash
POST http://localhost/v2/tokens/redeem
{"user_id": "<your-user-id>", "code": "<secret-code>"}
```
Tokens added = money × current price (default: 10 tokens per unit of money). Codes can only be used once.

## Interactive Docs
```
http://localhost/docs
```

## Logger Service
- Logs every request (time, username, endpoint) to daily CSV files in a Docker volume
- `POST http://localhost/v2/` requests are automatically logged
- Retention can be set via `POST logger:8000/retention` with `{"n": <days>}`

## Cache
GET requests to athlete, country and sport endpoints are cached in Redis for 60 seconds. Repeated identical requests within that window are served from cache without hitting the database.

## Rate Limiter
If a user makes 10 or more requests within 10 seconds, a delay is applied using `f(r) = r/10` seconds before the response is returned.
