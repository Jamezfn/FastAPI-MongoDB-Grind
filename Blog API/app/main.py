from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import init_db
from app.routers import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan"""
    await init_db()

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router=auth.router, prefix="/api/v1")