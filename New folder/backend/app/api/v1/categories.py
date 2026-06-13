from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category_service import CategoryService
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
async def list_categories(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    x_organization_id: str = Header(...)
):
    return await CategoryService.get_multi(db, x_organization_id)

@router.post("/", response_model=CategoryResponse)
async def create_category(
    request: CategoryCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    x_organization_id: str = Header(...)
):
    return await CategoryService.create(db, x_organization_id, request)
