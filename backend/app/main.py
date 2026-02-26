from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Literal
import uuid
from fastapi import FastAPI, HTTPException, status as http_status
from sqlmodel import func, select

from app.db import SessionDep, create_db_and_tables
from app.models import (
    Device,
    DeviceCreate,
    DeviceDetail,
    DeviceRead,
    DevicesPublic,
    Location,
    Overview,
    OverviewRead,
    Sensor,
    SensorData,
    SensorReading,
    Telemetry,
    TelemetryCreate,
    TelemetryPublic,
    TelemetryRead,
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


@app.get("/devices/{device_id}", response_model=DeviceDetail)
def read_device_by_id(device_id: uuid.UUID, session: SessionDep):
    """
    Read stats summary for a device
    """
    device = session.get(Device, device_id)
    if not device:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND, detail="Device not found"
        )

    stmt = (
        select(func.max(Telemetry.ts))
        .join(Sensor, Telemetry.sensor_id == Sensor.id)
        .where(Sensor.device_id == device.id)
    )
    last_seen = session.exec(stmt).one()
    device_status = (
        "online"
        if last_seen and last_seen > datetime.now() - timedelta(minutes=120)
        else "offline"
    )

    base_ts = device.last_reboot_ts or device.created_at

    uptime = None
    if device_status == "online":
        uptime_delta = datetime.now() - base_ts
        total_seconds = int(uptime_delta.total_seconds())

        uptime = {
            "days": uptime_delta.days,
            "hours": (total_seconds % 86400) // 3600,
            "minutes": (total_seconds % 3600) // 60,
            "seconds": total_seconds % 60,
            "total_seconds": total_seconds,
        }

    sensors = [sensor.model_dump() for sensor in device.sensors]

    return DeviceDetail(
        id=device.id,
        device_name=device.name,
        location_name=device.location.name,
        room=device.room,
        status=device_status,
        last_seen=last_seen or base_ts,
        uptime=uptime,
        sensors=sensors,
    )


# todo next
@app.get("/sensors/{sensor_id}/telemetry")
def read_device_telemetry(
    sensor_id: uuid.UUID,
    session: SessionDep,
    range: Literal["day", "week", "month", "year"],
):
    sensor = session.get(Sensor, sensor_id)
    if not sensor:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND, detail="Sensor not found"
        )

    # fetch telemetry per range
    # specify time resolution for each range
    # maybe day: hourly binning
    # week: daily averages
    # month: daily averages
    # year: monthly averages

    now = datetime.now()

    ranges = {
        "day": timedelta(days=1),
        "week": timedelta(weeks=1),
        "month": timedelta(days=30),
        "year": timedelta(days=365),
    }

    start = now - ranges[range]

    stmt = (
        select(
            func.date_trunc("hour", Telemetry.ts).label("ts_bin"),
            func.avg(Telemetry.value).label("mean"),
            func.min(Telemetry.value).label("min"),
            func.max(Telemetry.value).label("max"),
            func.count(),
        )
        .where(
            Telemetry.sensor_id == sensor_id,
            Telemetry.ts >= start,
        )
        .group_by("ts_bin")
        .order_by("ts_bin")
    )

    rows = session.exec(stmt).all()
    print(f"Rows: {rows}\n\nLen: {len(rows)}\n\n")

    data = [SensorData(ts=r.ts_bin, value=r.mean) for r in rows]

    return data


@app.post("/devices", response_model=DeviceRead)
def register_device(device_in: DeviceCreate, session: SessionDep):
    """Create a device, return id + api key, mainly used by devices on registration
    auto create device location if not exist
    """

    stmt = select(Device).where(Device.name == device_in.name).join(Location)
    device = session.exec(stmt).first()
    if device:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT, detail="Device already exists"
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
            status_code=http_status.HTTP_403_FORBIDDEN, detail="Sensor not found"
        )
    telemetry = Telemetry(**data.model_dump())
    session.add(telemetry)
    session.commit()
    session.refresh(telemetry)
    return telemetry
