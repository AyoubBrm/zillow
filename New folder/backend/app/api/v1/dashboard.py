from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.schemas.dashboard import DashboardSummary
from app.services.dashboard_service import DashboardService
from app.models.user import User

router = APIRouter()

@router.get("/summary", response_model=DashboardSummary)
async def get_summary(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    x_organization_id: str = Header(...)
):
    return await DashboardService.get_summary(db, x_organization_id)

@router.get("/trends")
async def get_trends(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    x_organization_id: str = Header(...)
):
    return await DashboardService.get_monthly_trends(db, x_organization_id)
