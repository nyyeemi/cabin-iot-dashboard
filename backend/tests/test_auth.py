from fastapi.testclient import TestClient


def test_missing_api_key(client: TestClient):
    res = client.get("/overview")
    assert res.status_code == 401
    assert res.json() == {"detail": "Not authenticated"}


def test_invalid_api_key(client: TestClient):
    res = client.get("/overview", headers={"X-API-Key": "wrong-key-123"})
    assert res.status_code == 401
    assert res.json() == {"detail": "Invalid api key"}


def test_valid_api_key(client: TestClient, monkeypatch):
    monkeypatch.setattr("app.auth.API_KEY", "test-secret-key")
    response = client.get("/overview", headers={"X-API-Key": "test-secret-key"})
    assert response.status_code == 200
