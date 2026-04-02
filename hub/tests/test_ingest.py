from unittest.mock import patch


def test_buffers_when_offline(client):
    with patch("app.main.is_connected", return_value=False):
        res = client.post(
            "/ingest",
            json={
                "ts": "2024-01-01T00:00:00Z",
                "value": 21.5,
                "sensor_id": "00000000-0000-0000-0000-000000000001",
            },
        )
    assert res.status_code == 200
    assert res.json()["msg"] == "buffered"


def test_forwards_when_online(client):
    with (
        patch("app.main.is_connected", return_value=True),
        patch("app.main.forward", return_value=True) as mock_fwd,
        patch("app.main.flush_buffer"),
    ):
        res = client.post(
            "/ingest",
            json={
                "ts": "2024-01-01T00:00:00Z",
                "value": 21.5,
                "sensor_id": "00000000-0000-0000-0000-000000000001",
            },
        )
    assert res.status_code == 200
    mock_fwd.assert_called_once()
