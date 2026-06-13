from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest, db: AsyncSession = Depends(deps.get_db)):
    return await AuthService.register(db, request)

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(deps.get_db)):
    return await AuthService.login(db, request.email, request.password)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(deps.get_current_user)):
    return current_user
