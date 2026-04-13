from contextlib import asynccontextmanager
from datetime import datetime, timezone
import os
import uuid

from fastapi import FastAPI
import httpx
from pydantic import BaseModel
import logging
import sqlite3


logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Hub starting — API_URL=%s", API_URL)
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")


def utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def init_db():
    con = sqlite3.connect("buffer.db")
    con.execute(
        "CREATE TABLE IF NOT EXISTS buffer (data TEXT NOT NULL, ts TEXT NOT NULL)"
    )
    con.commit()
    con.close()


class Telemetry(BaseModel):
    ts: datetime
    value: float
    sensor_id: uuid.UUID


def is_connected():
    try:
        res = httpx.get(f"{API_URL}/utils/health", timeout=3.0)
        return res.status_code == 200
    except Exception as e:
        logger.warning("Upstream unreachable, going offline", e)
        return False


def forward(telemetry: Telemetry) -> bool:
    try:
        r = httpx.post(
            f"{API_URL}/telemetry",
            json=telemetry.model_dump(mode="json"),
            headers={"X-API-Key": API_KEY},
        )
        r.raise_for_status()
        return True
    except httpx.HTTPError as e:
        logger.error("Forward failed for sensor_id=%s\n %s", telemetry.sensor_id, e)
        return False


def flush_buffer():
    con = sqlite3.connect("buffer.db")
    cur = con.cursor()
    rows = cur.execute("SELECT rowid, data FROM buffer ORDER BY ts ASC").fetchall()
    if rows:
        logger.info("Flushing %d buffered payloads", len(rows))
    for rowid, data in rows:
        if forward(Telemetry.model_validate_json(data)):
            cur.execute("DELETE FROM buffer WHERE rowid = ?", (rowid,))
            con.commit()
    con.close()


def buffer(payload: Telemetry):
    con = sqlite3.connect("buffer.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO buffer (data, ts) VALUES (?, ?)",
        (payload.model_dump_json(), utc_now().isoformat()),
    )
    con.commit()
    con.close()
    logger.warning("Buffered sensor_id=%s", payload.sensor_id)


@app.post("/ingest")
async def ingest(telemetry: Telemetry):
    if not is_connected():
        buffer(telemetry)
        return {"msg": "buffered"}

    flush_buffer()
    success = forward(telemetry)
    return success
