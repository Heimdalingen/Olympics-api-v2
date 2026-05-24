# IDG2001 — Assignment 2 Report

## Group Members
- Robin Heimdal (robinahe@stud.ntnu.no)

## Render URL (Assignment 1)
https://olympics-api-9xyt.onrender.com
(Note: free tier may have expired — run locally with docker compose up --build)

## GitHub Repository (Assignment 2)
https://github.com/Heimdalingen/Olympics-api-v2


---

## Introduction

This report reflects on the work done in Assignment 2 of IDG2001. The assignment built on top of Assignment 1, which was a REST API for querying Olympic Games data. The goal for Assignment 2 was to containerise the entire system using Docker Compose and extend it with several new microservices.

---

## What Was Built

The final system consists of 7 Docker containers:

- **Nginx** — reverse proxy and versioning server
- **Main API** — the FastAPI application (upgraded from v1 to v2)
- **Postgres** — replaced SQLite as the main database
- **Redis** — used as a cache layer for GET responses
- **Logger** — a separate microservice that writes request logs to daily CSV files
- **Rate Limiter** — tracks per-user request rates and applies delays when exceeded
- **Token Shop** — handles token purchases via one-time secret codes

---

## Reflections

### What Was Easy

Setting up the basic Docker Compose file and getting the containers running was relatively straightforward once the concepts were understood. FastAPI made it easy to build the three new microservices quickly, since the pattern was familiar from Assignment 1. Redis integration was also simpler than expected — the TTL feature built into Redis meant the cache expiry was handled automatically without any custom cleanup logic.

### What Was Hard

The most challenging part was getting the startup order right. Postgres takes a few seconds to be ready, and the main API would crash if it tried to connect before the database was ready. This was solved with a healthcheck on the Postgres container and a Python wait loop in the entrypoint script that retries the connection before seeding and starting the API.

YAML indentation in Docker Compose was also a source of several bugs early on — small mistakes like wrong indentation levels or typos in key names caused confusing error messages that took time to debug.

Switching from SQLite to Postgres required understanding the differences between the two — particularly around connection pooling (`pool_pre_ping`) and the connection string format.

### What Was Useful to Learn

Working through this assignment gave a much better understanding of how microservices communicate with each other inside a Docker network. Services can reach each other simply by using their container name as a hostname, which is a very clean way to handle internal networking.

The token shop flow — where a user buys a code from one service and redeems it through another — was a good practical example of how separate services can work together while keeping concerns separated. The one-time use code pattern also demonstrated a simple but effective way to prevent double-spending without needing a shared database between services.

Redis as a caching layer was a valuable concept to learn. The idea of storing frequently requested data temporarily to avoid repeated database queries is a fundamental performance optimisation in real-world APIs.

Overall, this assignment gave good hands-on experience with containerisation, microservice architecture, and the challenges that come with running multiple services together.

---

## Conclusion

Assignment 2 was significantly more complex than Assignment 1, but the added complexity reflected real-world backend architecture patterns. The combination of Docker Compose, multiple microservices, caching, rate limiting, and logging gave a broad overview of what a production-ready API system might look like.
