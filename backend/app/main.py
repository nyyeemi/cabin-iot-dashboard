from fastapi import FastAPI

from app.db import SessionDep, create_db_and_tables
from app.models.telemetry import Telemetry

app = FastAPI()


# todo: move to alembic, only for quick local dev
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/ingest")
async def ingest(data: Telemetry, session: SessionDep):
    print(data)
    session.add(data)
    session.commit()
    session.refresh(data)
    return data
