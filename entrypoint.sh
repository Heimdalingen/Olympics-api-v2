#!/bin/sh
set -e

# Wait for Postgres to be ready before starting
echo "Waiting for Postgres..."
python - <<'EOF'
import sys, time, os
from sqlalchemy import create_engine, text

url = os.environ["DATABASE_URL"]
for _ in range(30):
    try:
        engine = create_engine(url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Postgres is ready.")
        sys.exit(0)
    except Exception as e:
        print(f" not ready: {e}")
        time.sleep(2)
print("Postgres did not become ready in time.")
sys.exit(1)
EOF

# Seed the database with Olympic data
echo "Seeding database..."
python scripts/seed_db.py

# Start the API
echo "Starting API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
