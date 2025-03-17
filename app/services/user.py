from app.core.database import Database
from app.models.user import User

class UserService:
    collection_name = "users"

    @classmethod
    async def create_user(cls, user: User) -> bool:
        db = Database.get_db()
        existing_user = await db[cls.collection_name].find_one({"email": user.email})
        if existing_user:
            return False
        await db[cls.collection_name].insert_one(user.dict())
        return True

    @classmethod
    async def get_user_by_email(cls, email: str):
        db = Database.get_db()
        user = await db[cls.collection_name].find_one({"email": email})
        return user

    @classmethod
    async def update_refresh_token(cls, email: str, refresh_token: str):
        db = Database.get_db()
        await db[cls.collection_name].update_one(
            {"email": email},
            {"$set": {"refresh_token": refresh_token}}
        ) 