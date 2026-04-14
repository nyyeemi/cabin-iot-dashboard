import os
from typing import Annotated

from fastapi import Depends
from app import models  # noqa: F401
from sqlmodel import SQLModel, Session, create_engine


DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL, connect_args={"options": "-c timezone=UTC"})


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
