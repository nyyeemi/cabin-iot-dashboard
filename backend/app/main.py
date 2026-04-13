from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db import create_db_and_tables
from app.routes import main
from app.routes import utils


# todo: move to alembic, only for quick local dev
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(main.router)
app.include_router(utils.router)
