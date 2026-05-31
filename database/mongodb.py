from motor.motor_asyncio import AsyncIOMotorClient
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str
    MONGODB_DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

try:
    settings = Settings()
except Exception as e:
    print(f"Error loading settings: {e}")
    # Provide fallbacks if .env doesn't load cleanly in test environments
    class FallbackSettings:
        MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "fastapi_db")
        SECRET_KEY = os.getenv("SECRET_KEY", "secret")
        ALGORITHM = os.getenv("ALGORITHM", "HS256")
        ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    settings = FallbackSettings()

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def connect_to_mongo():
    try:
        db.client = AsyncIOMotorClient(settings.MONGODB_URL, serverSelectionTimeoutMS=2000)
        db.db = db.client[settings.MONGODB_DB_NAME]
        print("Initialized MongoDB client structure (Note: DNS or connection might fail if URI is dummy).")
    except Exception as e:
        print(f"Failed to initialize MongoDB client: {e}")
        print("WARNING: Make sure MONGODB_URL in .env is correct!")

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Closed MongoDB connection!")

def get_db():
    """Dependency to get the database instance."""
    return db.db
