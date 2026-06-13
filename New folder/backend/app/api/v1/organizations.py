from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.schemas.organization import OrgCreate, OrgResponse
from app.services.organization_service import OrganizationService
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=OrgResponse)
async def create_organization(
    request: OrgCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return await OrganizationService.create(db, current_user.id, request)

@router.get("/", response_model=List[OrgResponse])
async def list_organizations(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # This should return orgs the user is a member of. For simplicity, skipping full impl in MVP stub.
    pass
