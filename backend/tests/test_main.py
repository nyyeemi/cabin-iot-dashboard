from datetime import datetime
import uuid
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.db import get_session
from app.models import Device, Telemetry


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


def test_create_device(client: TestClient):
    response = client.post("/devices", json={"name": "esp32-c3"})
    data = response.json()

    assert response.status_code == 200
    assert data["id"] is not None


def test_create_device_incomplete(client: TestClient):
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
    device = Device(name=device_name)
    session.add(device)
    session.commit()

    response = client.post("/devices", json={"name": device_name})
    assert response.status_code == status.HTTP_409_CONFLICT


def test_read_device_by_id(session: Session, client: TestClient):
    device = Device(name="test-101")
    session.add(device)
    session.commit()
    session.refresh(device)

    response = client.get(f"/devices/{device.id}")
    data = response.json()

    assert data["name"] == "test-101"
    assert data["id"] is not None


def test_read_device_by_id_invalid(client: TestClient):
    response = client.get(f"/devices/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_read_devices(session: Session, client: TestClient):
    device_1 = Device(name="test-101")
    device_2 = Device(name="test-102")
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
