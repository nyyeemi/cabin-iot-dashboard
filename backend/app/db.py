import os
from typing import Annotated

from fastapi import Depends
from app import models  # noqa: F401
from sqlmodel import SQLModel, Session, create_engine

POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "example")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "cabin-iot")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")

postgres_url = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

engine = create_engine(postgres_url, connect_args={"options": "-c timezone=UTC"})


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def main():
    create_db_and_tables()


if __name__ == "__main__":
    main()
