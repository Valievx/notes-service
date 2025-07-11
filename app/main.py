from contextlib import asynccontextmanager

from fastapi import FastAPI

from common.settings import settings
from models.db_helper import db_helper
from api.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


def create_app():
    app = FastAPI(
        debug=settings.DEBUG,
        docs_url="/api/docs",
        title="Notes Manager",
        lifespan=lifespan,
    )
    app.include_router(router)
    return app
