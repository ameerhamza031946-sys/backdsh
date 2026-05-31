from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from database.mongodb import get_db
from schemas.user import UserCreate, UserResponse, UserLogin
from schemas.token import Token
from utils.hashing import get_password_hash, verify_password
from auth.jwt_handler import create_access_token
from models.helpers import user_helper

router = APIRouter()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db=Depends(get_db)):
    if await db["users"].find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
        
    user_dict = user.model_dump()
    user_dict["password"] = get_password_hash(user_dict["password"])
    
    new_user = await db["users"].insert_one(user_dict)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    return user_helper(created_user)

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db=Depends(get_db)):
    user = await db["users"].find_one({"email": user_credentials.email})
    if not user or not verify_password(user_credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
