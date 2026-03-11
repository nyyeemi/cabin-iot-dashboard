import os

from fastapi.testclient import TestClient
import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.db import get_session
from app.models import Sensor
from .test_main import (
    create_location_and_device,
    seed_sensor_telemetry_for_time_range,
)

POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "example")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "cabin-iot")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")

postgres_url = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(postgres_url)

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_read_device_telemetry(session: Session, client: TestClient):
    sensors = [
        Sensor(sensor_type="temperature", unit="celcius"),
        Sensor(sensor_type="humidity"),
    ]

    device, location = create_location_and_device(
        session=session, location_name="cabin", device_name="esp32", sensors=sensors
    )

    # seed some telemetry so last_seen and status can be computed
    seed_sensor_telemetry_for_time_range(
        session=session, sampling_interval=60, days=365
    )

    response = client.get(f"/sensors/{sensors[0].id}/telemetry?range=year")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 13

    response = client.get(f"/sensors/{sensors[0].id}/telemetry?range=month")

    assert response.status_code == 200
    data = response.json()

    print(len(data))

    response = client.get(f"/sensors/{sensors[0].id}/telemetry?range=week")

    assert response.status_code == 200
    data = response.json()

    print(len(data))

    response = client.get(f"/sensors/{sensors[0].id}/telemetry?range=day")

    assert response.status_code == 200
    data = response.json()
