#!/usr/bin/env python3
"""
Generated with claude.

Seed script for cabin IoT dashboard.
Populates the database with two locations, devices, sensors,
and a year of telemetry (6-hour intervals).

Usage:
    cd backend
    python scripts/seed.py

    # Or with a custom DB URL:
    DATABASE_URL=postgresql+psycopg://... python scripts/seed.py
"""

# ruff: noqa: E402
import math
import os
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Allow running from repo root or backend/
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from app.models import Device, Location, Sensor, Telemetry
from sqlmodel import Session, SQLModel, create_engine, select

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:example@localhost:5432/cabin-iot",
)

INTERVAL_HOURS = 6  # one reading every 6 hours → ~1460 rows per sensor per year

SEED_DATA = [
    {
        "location": "Mäntyranta",
        "devices": [
            {
                "name": "A-101",
                "room": "Upstairs",
                "sensors": [
                    {
                        "sensor_type": "temperature",
                        "unit": "°C",
                        "base": 18.0,
                        "amplitude": 6.0,
                    },
                    {
                        "sensor_type": "humidity",
                        "unit": "%",
                        "base": 55.0,
                        "amplitude": 15.0,
                    },
                ],
            },
            {
                "name": "A-102",
                "room": "Downstairs",
                "sensors": [
                    {
                        "sensor_type": "temperature",
                        "unit": "°C",
                        "base": 16.0,
                        "amplitude": 5.0,
                    },
                    {
                        "sensor_type": "humidity",
                        "unit": "%",
                        "base": 60.0,
                        "amplitude": 12.0,
                    },
                ],
            },
        ],
    },
    {
        "location": "Home",
        "devices": [
            {
                "name": "H-101",
                "room": "Living Room",
                "sensors": [
                    {
                        "sensor_type": "temperature",
                        "unit": "°C",
                        "base": 21.0,
                        "amplitude": 3.0,
                    },
                    {
                        "sensor_type": "humidity",
                        "unit": "%",
                        "base": 45.0,
                        "amplitude": 10.0,
                    },
                ],
            },
        ],
    },
]


# ---------------------------------------------------------------------------
# Telemetry generation
# ---------------------------------------------------------------------------


def generate_telemetry(
    sensor_id,
    base: float,
    amplitude: float,
    interval_hours: int = INTERVAL_HOURS,
) -> list[Telemetry]:
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=365)
    rows = []
    ts = start
    i = 0
    while ts <= now:
        # Seasonal sine wave (period = 1 year) + daily variation + noise
        day_of_year = (ts - start).days
        seasonal = amplitude * math.sin(2 * math.pi * day_of_year / 365 - math.pi / 2)
        noise = random.gauss(0, amplitude * 0.05)
        value = round(base + seasonal + noise, 2)
        rows.append(Telemetry(sensor_id=sensor_id, ts=ts, value=value))
        ts += timedelta(hours=interval_hours)
        i += 1
    return rows


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def seed():
    print(f"Connecting to: {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        total_telemetry = 0

        for loc_data in SEED_DATA:
            # Upsert location
            location = session.exec(
                select(Location).where(Location.name == loc_data["location"])
            ).first()
            if not location:
                location = Location(name=loc_data["location"])
                session.add(location)
                session.flush()
                print(f"  Created location: {location.name}")
            else:
                print(f"  Location exists, skipping: {location.name}")

            for dev_data in loc_data["devices"]:
                # Upsert device
                device = session.exec(
                    select(Device).where(
                        Device.name == dev_data["name"],
                        Device.location_id == location.id,
                    )
                ).first()
                if not device:
                    device = Device(
                        name=dev_data["name"],
                        room=dev_data["room"],
                        location=location,
                    )
                    session.add(device)
                    session.flush()
                    print(f"    Created device: {device.name} ({dev_data['room']})")
                else:
                    print(f"    Device exists, skipping: {device.name}")

                for sen_data in dev_data["sensors"]:
                    # Upsert sensor
                    sensor = session.exec(
                        select(Sensor).where(
                            Sensor.device_id == device.id,
                            Sensor.sensor_type == sen_data["sensor_type"],
                        )
                    ).first()
                    if not sensor:
                        sensor = Sensor(
                            sensor_type=sen_data["sensor_type"],
                            unit=sen_data["unit"],
                            device=device,
                        )
                        session.add(sensor)
                        session.flush()
                        print(f"      Created sensor: {sensor.sensor_type}")
                    else:
                        print(f"      Sensor exists, skipping: {sensor.sensor_type}")

                    # Always (re)seed telemetry — wipe existing for this sensor first
                    existing = session.exec(
                        select(Telemetry).where(Telemetry.sensor_id == sensor.id)
                    ).all()
                    if existing:
                        for t in existing:
                            session.delete(t)
                        session.flush()
                        print(f"        Wiped {len(existing)} existing telemetry rows")

                    rows = generate_telemetry(
                        sensor_id=sensor.id,
                        base=sen_data["base"],
                        amplitude=sen_data["amplitude"],
                    )
                    session.add_all(rows)
                    total_telemetry += len(rows)
                    print(f"        Seeded {len(rows)} telemetry rows")

        session.commit()
        print(f"\nDone. {total_telemetry} telemetry rows committed.")


if __name__ == "__main__":
    random.seed(42)
    seed()
