import uuid

from sqlmodel import Session, select

from app.models import Telemetry


def sensor_get_latest_telemetry(*, session: Session, sensor_id: uuid.UUID):
    statement = (
        select(Telemetry)
        .where(Telemetry.sensor_id == sensor_id)
        .order_by(Telemetry.ts.desc())
    )
    latest = session.exec(statement).first()
    return latest
