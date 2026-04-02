# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(name="client")
def client_fixture(tmp_path, monkeypatch):
    monkeypatch.setenv("API_URL", "http://fake-railway.com")
    monkeypatch.setenv("API_KEY", "test-key")

    monkeypatch.chdir(tmp_path)

    with TestClient(app) as client:
        yield client
