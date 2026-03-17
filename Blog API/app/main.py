from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import init_db
from app.routers import auth, user, post, comment

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan"""
    await init_db() 

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router=auth.router, prefix="/api/v1")
app.include_router(router=user.router, prefix="/api/v1")
app.include_router(router=post.router, prefix="/api/v1")
app.include_router(router=comment.router, prefix="/api/v1")