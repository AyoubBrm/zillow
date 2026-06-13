from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.schemas.ai import CategorizationRequest, CategorizationResponse
from app.ai.categorizer import Categorizer
from app.models.user import User

router = APIRouter()
categorizer = Categorizer()

@router.post("/categorize", response_model=CategorizationResponse)
async def categorize_transaction(
    request: CategorizationRequest,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    x_organization_id: str = Header(...)
):
    result = await categorizer.categorize(request.description, request.amount)
    return CategorizationResponse(
        category=result.category,
        confidence=result.confidence
    )
