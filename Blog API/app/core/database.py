from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.models.user import User
from app.models.tags import Tag
from app.models.post import Post
from app.models.comment import Comment
from app.config import settings

async def init_db():
    client = AsyncIOMotorClient(settings.database_url)
    await client.admin.command('ping')
    db = client[settings.db_name]
    await init_beanie(database=db, document_models=[User, Tag, Post, Comment])