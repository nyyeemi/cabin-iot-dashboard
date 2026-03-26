from fastapi.testclient import TestClient


def test_missing_api_key(client_no_auth: TestClient):
    res = client_no_auth.get("/overview")
    assert res.status_code == 401
    assert res.json() == {"detail": "Not authenticated"}


def test_invalid_api_key(client_no_auth: TestClient):
    res = client_no_auth.get("/overview", headers={"X-API-Key": "wrong-key-123"})
    assert res.status_code == 401
    assert res.json() == {"detail": "Invalid api key"}


def test_valid_api_key(client_no_auth: TestClient, monkeypatch):
    monkeypatch.setattr("app.auth.API_KEY", "test-secret-key")
    response = client_no_auth.get("/overview", headers={"X-API-Key": "test-secret-key"})
    assert response.status_code == 200
