import os
from pymongo import AsyncMongoClient
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("MONGODB_URL")

client = AsyncMongoClient(host=DATABASE_URL)
db = client.college

student_collection = db.get_collection("students")