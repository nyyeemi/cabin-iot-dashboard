from datetime import timedelta
import math
import random
import time

from sqlmodel import Session, select

from app.models import Device, Location, Sensor, Telemetry
from app.utils import utc_now


def create_location_and_device(
    *, session: Session, location_name: str, device_name: str, sensors: list[Sensor]
):
    location = Location(name=location_name)
    session.add(location)
    session.commit()

    device = Device(name=device_name, location_id=location.id, sensors=sensors)
    session.add(device)
    session.commit()

    return device, location


def seed_sensor_telemetry(*, session=Session, n: int = 5):
    sensors = session.exec(select(Sensor)).all()

    telemetries = []
    for sensor in sensors:
        for i in range(n):
            ts = utc_now()
            value = random.gauss(mu=20, sigma=5)
            telemetries.append(Telemetry(ts=ts, value=value, sensor_id=sensor.id))
            time.sleep(0.01)

    session.add_all(telemetries)
    session.commit()


def seed_sensor_telemetry_for_time_range(
    *, session=Session, sampling_interval: int = 60, days: int = 1
):
    """sampling_interval in minutes"""

    sensors = session.exec(select(Sensor)).all()

    telemetries = []
    n = math.ceil(days * 24 * 60 / sampling_interval)
    now = utc_now()

    for sensor in sensors:
        for i in range(n):
            ts = now - timedelta(minutes=i * sampling_interval)
            value = random.gauss(mu=20, sigma=5)
            telemetries.append(Telemetry(ts=ts, value=value, sensor_id=sensor.id))

    session.add_all(telemetries)
    session.commit()
