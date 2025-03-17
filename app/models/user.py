from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserInDB(BaseModel):
    email: EmailStr
    hashed_password: str
    full_name: str
    created_at: datetime = datetime.utcnow()
    refresh_token: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "hashed_password": "hashed_password_here",
                "full_name": "John Doe",
                "created_at": datetime.utcnow(),
                "refresh_token": None
            }
        } 