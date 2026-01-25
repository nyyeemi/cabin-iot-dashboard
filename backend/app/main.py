import uuid
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlmodel import select

from app.db import SessionDep, create_db_and_tables
from app.models import Telemetry, Device

app = FastAPI()


# todo: move to alembic, only for quick local dev
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


class DeviceIn(BaseModel):
    name: str


class RegisterResponse(BaseModel):
    device_id: uuid.UUID


@app.post("/devices/register", response_model=RegisterResponse)
def register_device(device_in: DeviceIn, session: SessionDep):
    """Initiate a new device and assign uuid to it."""
    stmt = select(Device).where(Device.name == device_in.name)
    device = session.exec(stmt).first()
    if device is None:
        device = Device(name=device_in.name)
        session.add(device)
        session.commit()
        session.refresh(device)
    return {"device_id": device.id}


@app.post("/ingest")
def ingest(data: Telemetry, session: SessionDep):
    device = session.get(Device, data.device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Device not registered"
        )
    session.add(data)
    session.commit()
    session.refresh(data)
    return data
