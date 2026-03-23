from datetime import datetime
import uuid

from sqlmodel import Session, func, select

from app.models import Device, Sensor, Telemetry


def sensor_get_latest_telemetry(*, session: Session, sensor_id: uuid.UUID):
    statement = (
        select(Telemetry)
        .where(Telemetry.sensor_id == sensor_id)
        .order_by(Telemetry.ts.desc())
    )
    latest = session.exec(statement).first()
    return latest


def device_get_latest_reading_timestamp(
    *, session: Session, device: Device
) -> datetime | None:
    stmt = (
        select(func.max(Telemetry.ts))
        .join(Sensor, Telemetry.sensor_id == Sensor.id)
        .where(Sensor.device_id == device.id)
    )
    last_seen = session.exec(stmt).one_or_none()

    return last_seen
