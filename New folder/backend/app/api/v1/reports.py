from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import date

from app.api import deps
from app.schemas.report import ReportRequest, ReportResponse
from app.services.report_service import ReportService
from app.models.user import User

router = APIRouter()

@router.post("/generate", response_model=ReportResponse)
async def generate_report(
    request: ReportRequest,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    x_organization_id: str = Header(...)
):
    if request.type == "profit_loss":
        return await ReportService.generate_profit_loss(db, x_organization_id, request.period_start, request.period_end)
    # MVP fallback
    return ReportResponse(id="temp", organization_id=x_organization_id, type=request.type, period_start=request.period_start, period_end=request.period_end, data={}, status="error")
