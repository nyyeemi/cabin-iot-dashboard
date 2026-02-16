from contextlib import asynccontextmanager
import uuid
from fastapi import FastAPI, HTTPException, status
from sqlmodel import func, select

from app.db import SessionDep, create_db_and_tables
from app.models import (
    Device,
    DeviceCreate,
    DeviceRead,
    DevicesPublic,
    Location,
    Overview,
    OverviewRead,
    Sensor,
    SensorReading,
    Telemetry,
    TelemetryCreate,
    TelemetryPublic,
)
from app.crud import sensor_get_latest_telemetry


# todo: move to alembic, only for quick local dev
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/overview", response_model=OverviewRead)
def read_overview(session: SessionDep):
    """
    Read location based overview for dashboards summary page.
    todo: should be fetched for current user
    """

    locations = session.exec(select(Location)).all()

    overviews = []

    for location in locations:
        overview_dict = {
            "location_id": location.id,
            "location_name": location.name,
            "devices": [],
        }
        devices = location.devices

        for device in devices:
            device_overview = {"device_id": device.id, "device_name": device.name}
            sensors = device.sensors
            latest_readings = []
            for sensor in sensors:
                latest_reading = sensor_get_latest_telemetry(
                    session=session, sensor_id=sensor.id
                )

                latest_readings.append(
                    {
                        "sensor_type": sensor.sensor_type,
                        "unit": sensor.unit,
                        "value": latest_reading.value,
                        "ts": latest_reading.ts,
                    }
                )

            device_overview["latest_readings"] = latest_readings
            overview_dict["devices"].append(device_overview)

        overviews.append(overview_dict)

    return OverviewRead(data=overviews)


@app.post("/devices", response_model=DeviceRead)
def register_device(device_in: DeviceCreate, session: SessionDep):
    """Create a device, return id + api key, mainly used by devices on registration
    auto create device location if not exist
    """

    stmt = select(Device).where(Device.name == device_in.name).join(Location)
    device = session.exec(stmt).first()
    if device:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Device already exists"
        )

    location = session.exec(
        select(Location).where(Location.name == device_in.location_name)
    ).first()

    if location is None:
        location = Location(name=device_in.location_name)
        session.add(location)

    device = Device(name=device_in.name, location=location)

    sensors = [Sensor(**sensor.model_dump()) for sensor in device_in.sensors]
    device.sensors = sensors

    session.add(device)
    session.commit()
    session.refresh(device)
    return DeviceRead(
        id=device.id,
        name=device.name,
        location_name=location.name,
        sensors=device.sensors,
    )


@app.post("/telemetry")
def ingest(data: TelemetryCreate, session: SessionDep):
    sensor = session.get(Sensor, data.sensor_id)
    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Sensor not found"
        )
    telemetry = Telemetry(**data.model_dump())
    session.add(telemetry)
    session.commit()
    session.refresh(telemetry)
    return telemetry


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# all definitions below are deprecated. needs refactoring + testing after schema change


@app.get("/devices", response_model=DevicesPublic)
def read_devices(session: SessionDep, offset: int = 0, limit: int = 100):
    count_statement = select(func.count()).select_from(Device)
    count = session.exec(count_statement).one()

    devices = session.exec(select(Device).offset(offset).limit(limit)).all()

    return DevicesPublic(data=devices, count=count)


@app.get("/devices/{device_id}", response_model=DeviceRead)
def read_device_by_id(device_id: uuid.UUID, session: SessionDep):
    device = session.get(Device, device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Device not found"
        )
    return DeviceRead(
        id=device.id, name=device.name, location_name=device.location.name
    )


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
