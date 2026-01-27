from contextlib import asynccontextmanager
import uuid
from fastapi import FastAPI, HTTPException, status
from sqlmodel import func, select

from app.db import SessionDep, create_db_and_tables
from app.models import (
    Device,
    DeviceCreate,
    DeviceCreateResponse,
    DevicesPublic,
    Telemetry,
    TelemetryCreate,
    TelemetryPublic,
)


# todo: move to alembic, only for quick local dev
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/devices", response_model=DevicesPublic)
def read_devices(session: SessionDep, offset: int = 0, limit: int = 100):
    count_statement = select(func.count()).select_from(Device)
    count = session.exec(count_statement).one()

    devices = session.exec(select(Device).offset(offset).limit(limit)).all()

    return DevicesPublic(data=devices, count=count)


@app.post("/devices", response_model=DeviceCreateResponse)
def register_device(device_in: DeviceCreate, session: SessionDep):
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


@app.get("/devices/{device_id}/telemetry", response_model=list[TelemetryPublic])
def read_device_telemetry(device_id: uuid.UUID, session: SessionDep):
    device = session.get(Device, device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Device not found"
        )
    statement = select(Telemetry).where(Telemetry.device_id == device_id)
    telemetry_data = session.exec(statement).all()
    return telemetry_data


@app.get("/devices/{device_id}/telemetry/latest", response_model=TelemetryPublic)
def read_device_telemetry_latest(device_id: uuid.UUID, session: SessionDep):
    device = session.get(Device, device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Device not found"
        )
    statement = (
        select(Telemetry)
        .where(Telemetry.device_id == device_id)
        .order_by(Telemetry.ts.desc())
    )
    latest = session.exec(statement).first()
    return latest


# NOTE: /ingest for raspi, change to more restful /telemetry here
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
