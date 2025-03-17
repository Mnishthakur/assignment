from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from app.schemas.auth import UserCreate, UserLogin, Token, UserResponse
from app.services.auth import AuthService
from app.core.database import Database
from app.models.user import UserInDB

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = AuthService.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await Database.get_db()["users"].find_one({"email": payload.get("sub")})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/register", response_model=dict)
async def register(user_data: UserCreate):
    hashed_password = AuthService.get_password_hash(user_data.password)
    user = UserInDB(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name
    )
    
    # Check if user exists
    existing_user = await Database.get_db()["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Insert new user
    await Database.get_db()["users"].insert_one(user.dict())
    return {"message": "User registered successfully"}

@router.post("/login", response_model=Token)
async def login(response: Response, user_data: UserLogin):
    user = await Database.get_db()["users"].find_one({"email": user_data.email})
    if not user or not AuthService.verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = AuthService.create_access_token({"sub": user["email"]})
    refresh_token = AuthService.create_refresh_token({"sub": user["email"]})
    
    # Update refresh token in database
    await Database.get_db()["users"].update_one(
        {"email": user["email"]},
        {"$set": {"refresh_token": refresh_token}}
    )
    
    # Set cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=60 * 1  # 1 minute
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=60 * 60 * 24 * 7  # 1 week
    )
    
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.get("/me", response_model=UserResponse)
async def get_user_details(current_user: dict = Depends(get_current_user)):
    return {"email": current_user["email"], "full_name": current_user["full_name"]} 