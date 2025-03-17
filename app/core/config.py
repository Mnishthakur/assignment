from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    database_name: str = os.getenv("DATABASE_NAME", "auth_db")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-for-jwt")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    port: int = int(os.getenv("PORT", "8001"))

    class Config:
        case_sensitive = True

settings = Settings() 