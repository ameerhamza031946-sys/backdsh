from fastapi import APIRouter, Depends
from schemas.user import UserResponse
from auth.deps import get_current_user

router = APIRouter()

@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
