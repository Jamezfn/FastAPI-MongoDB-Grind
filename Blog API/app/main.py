from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import init_db
from app.routers import auth, user, post, comment

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan"""
    await init_db() 

    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=auth.router, prefix="/api/v1")
app.include_router(router=user.router, prefix="/api/v1")
app.include_router(router=post.router, prefix="/api/v1")
app.include_router(router=comment.router, prefix="/api/v1")