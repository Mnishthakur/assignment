from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123",
                "full_name": "John Doe"
            }
        }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123"
            }
        }

class Token(BaseModel):
    access_token: str
    refresh_token: str

class UserResponse(BaseModel):
    email: EmailStr
    full_name: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "full_name": "John Doe"
            }
        } 