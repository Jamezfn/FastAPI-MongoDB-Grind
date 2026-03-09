# from motor.motor_asyncio import AsyncIOMotorClient
# from beanie import init_beanie
# import os

# from app.models.user import User
# from app.models.tag import Tag
# from app.models.category import Category
# from app.models.post import Post
# from app.models.comment import Comment

# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/mydb")

# async def init_db():
#     client = AsyncIOMotorClient(MONGO_URI)
#     db = client.get_default_database()
#     await init_beanie(database=db, document_models=[User, Tag, Category, Post, Comment])