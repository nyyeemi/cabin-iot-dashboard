import os

from fastapi.testclient import TestClient
import pytest
from sqlmodel import SQLModel, Session, StaticPool, create_engine
from app.main import app
from app.db import get_session
from app.auth import verify_api_key


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client_no_auth")
def unauthorized_client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[verify_api_key] = lambda: True

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="pg_session")
def pg_session_fixture():
    engine = create_engine(
        url=os.environ.get(
            "TEST_DATABASE_URL",
            "postgresql+psycopg://postgres:example@localhost:5432/cabin-iot",
        ),
    )

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="pg_client")
def pg_client_fixture(pg_session: Session):
    def get_session_override():
        return pg_session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[verify_api_key] = lambda: True

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
