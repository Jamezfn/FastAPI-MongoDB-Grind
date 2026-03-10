from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan"""
    await init_db()

    yield

app = FastAPI(lifespan=lifespan)