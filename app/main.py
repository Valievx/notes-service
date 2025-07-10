from contextlib import asynccontextmanager

from fastapi import FastAPI

from common.settings import settings
from models.db_helper import DatabaseHelper


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_helper = DatabaseHelper(url=str(settings.DATABASE_URL))
    yield
    await db_helper.dispose()


def create_app():
    app = FastAPI(
        debug=settings.DEBUG,
        docs_url="/api/docs",
        title="Notes Manager",
        lifespan=lifespan,
    )

    return app
