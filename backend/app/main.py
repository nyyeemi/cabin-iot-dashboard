from contextlib import asynccontextmanager
import uuid
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlmodel import SQLModel, func, select

from app.db import SessionDep, create_db_and_tables
from app.models import Device, Telemetry, TelemetryCreate


# todo: move to alembic, only for quick local dev
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


class DeviceIn(BaseModel):
    name: str


class RegisterResponse(BaseModel):
    id: uuid.UUID


class DevicesPublic(SQLModel):
    data: list[Device]
    count: int


@app.get("/devices", response_model=DevicesPublic)
def read_devices(session: SessionDep, offset: int = 0, limit: int = 100):
    count_statement = select(func.count()).select_from(Device)
    count = session.exec(count_statement).one()

    devices = session.exec(select(Device).offset(offset).limit(limit)).all()

    return DevicesPublic(data=devices, count=count)


@app.post("/devices", response_model=RegisterResponse)
def register_device(device_in: DeviceIn, session: SessionDep):
    """Create a device, return id + api key, mainly used by devices on registration"""
    stmt = select(Device).where(Device.name == device_in.name)
    device = session.exec(stmt).first()
    if device:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Device already exists"
        )

    device = Device(name=device_in.name)
    session.add(device)
    session.commit()
    session.refresh(device)
    return {"id": device.id}


@app.get("/devices/{device_id}", response_model=Device)
def read_device_by_id(device_id: uuid.UUID, session: SessionDep):
    device = session.get(Device, device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Device not found"
        )
    return device


@app.post("/ingest")
def ingest(data: TelemetryCreate, session: SessionDep):
    device = session.get(Device, data.device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Device not registered"
        )
    telemetry = Telemetry(**data.model_dump())
    session.add(telemetry)
    session.commit()
    session.refresh(telemetry)
    return telemetry
