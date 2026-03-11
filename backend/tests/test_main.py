from datetime import datetime, timedelta, timezone
import math
import random
import time
import uuid
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from sqlmodel import SQLModel, Session, create_engine, select
from sqlmodel.pool import StaticPool
from app.main import app
from app.db import get_session
from app.models import Device, Location, Sensor, Telemetry


# crud
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
            ts = datetime.now(tz=timezone.utc)
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
    now = datetime.now(tz=timezone.utc)

    for sensor in sensors:
        for i in range(n):
            ts = now - timedelta(minutes=i * sampling_interval)
            value = random.gauss(mu=20, sigma=5)
            telemetries.append(Telemetry(ts=ts, value=value, sensor_id=sensor.id))

    session.add_all(telemetries)
    session.commit()


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
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


def test_create_device(session: Session, client: TestClient):
    sensors = [
        {"sensor_type": "temperature", "unit": "celcius"},
        {"sensor_type": "humidity"},
    ]
    payload = {"name": "esp32-c3", "location_name": "cabin", "sensors": sensors}

    response = client.post("/devices", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["id"] is not None
    assert data["location_name"] == "cabin"
    assert len(data["sensors"]) == 2

    device = session.get(Device, uuid.UUID(data["id"]))
    assert device is not None
    assert device.location.name == "cabin"
    assert len(device.sensors) == 2

    sensor_types = {s.sensor_type for s in device.sensors}
    assert "temperature" in sensor_types
    assert "humidity" in sensor_types


def test_create_telemetry(session: Session, client: TestClient):
    sensors = [
        Sensor(sensor_type="temperature", unit="celcius"),
        Sensor(sensor_type="humidity"),
    ]

    device, _ = create_location_and_device(
        session=session, location_name="test", device_name="test", sensors=sensors
    )
    ts = datetime.now(tz=timezone.utc).isoformat()
    sensor_id = str(device.sensors[0].id)
    payload = {"ts": ts, "value": 20.2, "sensor_id": sensor_id}
    response = client.post("/telemetry", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["sensor_id"] == sensor_id


def test_read_overview(session: Session, client: TestClient):
    sensors = [
        Sensor(sensor_type="temperature", unit="celcius"),
        Sensor(sensor_type="humidity"),
    ]

    device, _ = create_location_and_device(
        session=session, location_name="test", device_name="test", sensors=sensors
    )

    seed_sensor_telemetry(session=session, n=5)

    response = client.get("/overview")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    location = data["data"][0]

    assert location["location_name"] == "test"
    assert len(location["devices"]) == 1

    device = location["devices"][0]
    assert device["device_name"] == "test"
    assert {r["sensor_type"] for r in device["latest_readings"]} == {
        "temperature",
        "humidity",
    }


def test_read_device_detail(session: Session, client: TestClient):
    sensors = [
        Sensor(sensor_type="temperature", unit="celcius"),
        Sensor(sensor_type="humidity"),
    ]

    device, location = create_location_and_device(
        session=session, location_name="cabin", device_name="esp32", sensors=sensors
    )

    # seed some telemetry so last_seen and status can be computed
    seed_sensor_telemetry(session=session, n=1)

    response = client.get(f"/devices/{device.id}")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == str(device.id)
    assert data["device_name"] == "esp32"
    assert data["location_name"] == "cabin"
    assert data["status"] == "online"
    assert "last_seen" in data
    assert "uptime" in data
    assert len(data["sensors"]) == 2


""" def test_create_device_incomplete(client: TestClient):
    response = client.post("/devices")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_device_invalid(client: TestClient):
    response = client.post(
        "/devices",
        json={"name": 600},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_device_duplicate(session: Session, client: TestClient):
    device_name = "i-already-exist"
    location = Location(name="cabin")
    session.add(location)
    session.commit()

    device = Device(name=device_name, location_id=location.id)
    session.add(device)
    session.commit()

    response = client.post(
        "/devices", json={"name": device_name, "location_name": location.name}
    )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_device_location_auto_create(session: Session, client: TestClient):
    #Test that device registration works whether the location exists or not.

    # loc does not exist yet
    new_location_name = "new-cabin"
    response = client.post(
        "/devices", json={"name": "esp32-new", "location_name": new_location_name}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["id"] is not None
    assert data["location_name"] == new_location_name

    location_in_db = session.exec(
        select(Location).where(Location.name == new_location_name)
    ).first()
    assert location_in_db is not None

    # loc already exists
    existing_location_name = new_location_name
    response2 = client.post(
        "/devices",
        json={"name": "esp32-existing", "location_name": existing_location_name},
    )
    data2 = response2.json()
    assert response2.status_code == 200
    assert data2["location_name"] == existing_location_name

    # check no new locations added to db
    locations_in_db = session.exec(select(Location)).all()
    assert len(locations_in_db) == 1


def test_read_device_by_id(session: Session, client: TestClient):
    device, location = create_location_and_device(
        session, location_name="loc-1", device_name="d-101"
    )

    response = client.get(f"/devices/{device.id}")
    data = response.json()

    assert data["name"] == "d-101"
    assert data["id"] is not None
    assert data["location_name"] == "loc-1"


def test_read_device_by_id_invalid(client: TestClient):
    response = client.get(f"/devices/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


## fix tests below
def test_read_devices(session: Session, client: TestClient):
    location = Location(name="loc")
    session.add(location)
    session.commit()

    device_1 = Device(name="test-101", location_id=location.id)
    device_2 = Device(name="test-102", location_id=location.id)
    session.add(device_1)
    session.add(device_2)
    session.commit()

    response = client.get("/devices/")
    data = response.json()
    devices = data["data"]

    assert response.status_code == 200

    assert data["count"] == 2
    assert devices[0]["name"] == device_1.name
    assert devices[0]["id"] == str(device_1.id)
    assert devices[1]["name"] == device_2.name
    assert devices[1]["id"] == str(device_2.id)


def test_read_device_telemetry(session: Session, client: TestClient):
    device = Device(name="test-101")
    session.add(device)
    session.commit()

    telemetry_1 = Telemetry(device_id=device.id, ts=datetime.now(), temp=21.5)
    telemetry_2 = Telemetry(device_id=device.id, ts=datetime.now(), temp=21.6)
    session.add_all([telemetry_1, telemetry_2])
    session.commit()
    response = client.get(f"/devices/{device.id}/telemetry")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2

    assert data[0]["device_id"] == str(device.id)
    assert data[0]["temp"] == telemetry_1.temp
    assert data[0]["ts"] == telemetry_1.ts.isoformat()

    assert data[1]["device_id"] == str(device.id)
    assert data[1]["temp"] == telemetry_2.temp
    assert data[1]["ts"] == telemetry_2.ts.isoformat()


def test_read_device_telemetry_latest(session: Session, client: TestClient):
    device = Device(name="test-101")
    session.add(device)
    session.commit()

    telemetry_1 = Telemetry(device_id=device.id, ts=datetime.now(), temp=21.5)
    telemetry_2 = Telemetry(device_id=device.id, ts=datetime.now(), temp=21.6)
    session.add_all([telemetry_1, telemetry_2])
    session.commit()
    response = client.get(f"/devices/{device.id}/telemetry/latest")

    assert response.status_code == 200

    data = response.json()
    assert data["device_id"] == str(device.id)
    assert data["temp"] == telemetry_2.temp
    assert data["ts"] == telemetry_2.ts.isoformat()


# -----------------/ingest-----------------------
#
#
#
#
#
def test_ingest(session: Session, client: TestClient):
    device = Device(name="test")
    session.add(device)
    session.commit()

    ts = datetime.now().isoformat()
    temp = 0.9
    id = str(device.id)

    payload = {"device_id": id, "temp": temp, "ts": ts}
    print(payload)
    response = client.post("/ingest", json=payload)

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["device_id"] == str(device.id)
    assert data["ts"] == ts
    assert data["temp"] == temp


def test_ingest_unknown_device(session: Session, client: TestClient):
    payload = {"device_id": str(uuid.uuid4()), "temp": 0.1, "ts": str(datetime.now())}
    response = client.post("/ingest", json=payload)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_ingest_incomplete(client: TestClient):
    response = client.post("/ingest")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_ingest_invalid(client: TestClient):
    response = client.post(
        "/ingest",
        json={"name": 600, "device_id": 30},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


# add test "/devices/{device_id}/telemetry/latest", so that device defined but does not contain data, throws error now
 """
