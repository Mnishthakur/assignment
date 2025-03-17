from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    
    @classmethod
    async def connect_db(cls):
        try:
            cls.client = AsyncIOMotorClient(settings.mongodb_url)
            await cls.client.admin.command('ping')
            print("Connected to MongoDB!")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise e
            
    @classmethod
    async def close_db(cls):
        if cls.client is not None:
            cls.client.close()
            
    @classmethod
    def get_db(cls):
        if cls.client is None:
            raise Exception("Database client not initialized. Call connect_db first.")
        return cls.client[settings.database_name] 