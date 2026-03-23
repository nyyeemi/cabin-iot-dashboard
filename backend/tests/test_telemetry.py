from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models import Sensor
from tests.factories import (
    create_location_and_device,
    seed_sensor_telemetry_for_time_range,
)


def test_read_device_telemetry(pg_session: Session, pg_client: TestClient):
    sensors = [
        Sensor(sensor_type="temperature", unit="celcius"),
        Sensor(sensor_type="humidity"),
    ]

    device, location = create_location_and_device(
        session=pg_session, location_name="cabin", device_name="esp32", sensors=sensors
    )

    # seed some telemetry so last_seen and status can be computed
    seed_sensor_telemetry_for_time_range(
        session=pg_session, sampling_interval=60, days=365
    )

    response = pg_client.get(f"/sensors/{sensors[0].id}/telemetry?range=year")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 13

    response = pg_client.get(f"/sensors/{sensors[0].id}/telemetry?range=month")

    assert response.status_code == 200
    data = response.json()

    print(len(data))

    response = pg_client.get(f"/sensors/{sensors[0].id}/telemetry?range=week")

    assert response.status_code == 200
    data = response.json()

    print(len(data))

    response = pg_client.get(f"/sensors/{sensors[0].id}/telemetry?range=day")

    assert response.status_code == 200
    data = response.json()
