import csv
import glob
import os
from datetime import date, datetime

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Logger Service")

LOG_DIR = "/logs"
log_buffer: list = []
retention_days: int = 7

class LogEntry(BaseModel):
    username: str
    endpoint: str

class RetentionConfig(BaseModel):
    n: int

def get_log_path() -> str:
    return os.path.join(LOG_DIR, f"log_{date.today().isoformat()}.csv")


def flush_to_csv(entries: list) -> None:
    if not entries:
        return
    os.makedirs(LOG_DIR, exist_ok=True)
    path = get_log_path()
    file_exists = os.path.isfile(path)
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["time", "username", "endpoint"])
        writer.writerows(entries)


@app.post("/log")
def log_request(entry: LogEntry):
    log_buffer.append((datetime.utcnow().isoformat(), entry.username, entry.endpoint))
    flush_to_csv(log_buffer.copy())
    log_buffer.clear()
    return {"status": "logged"}

@app.post("/retention")
def set_retention(config: RetentionConfig):
    global retention_days
    retention_days = config.n
    today = date.today()
    for filepath in glob.glob(os.path.join(LOG_DIR, "log_*.csv")):
        name = os.path.basename(filepath)
        try:
            file_date = date.fromisoformat(name[4:-4])
            if (today - file_date).days > retention_days:
                os.remove(filepath)
        except ValueError:
            pass
    return {"retention_days": retention_days}