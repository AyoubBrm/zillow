from fastapi import APIRouter, Depends, UploadFile, File, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.schemas.transaction import TransactionResponse, TransactionCreate
from app.services.transaction_service import TransactionService
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[TransactionResponse])
async def list_transactions(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    x_organization_id: str = Header(...)
):
    return await TransactionService.get_multi(db, x_organization_id)

@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    request: TransactionCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    x_organization_id: str = Header(...)
):
    return await TransactionService.create(db, x_organization_id, request)

@router.post("/import", response_model=dict)
async def import_transactions(
    account_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    x_organization_id: str = Header(...)
):
    from app.services.import_service import ImportService
    content = await file.read()
    transactions = await ImportService.parse_file(content, file.filename, x_organization_id, account_id)
    # Save parsed transactions
    saved = 0
    for t in transactions:
        try:
            await TransactionService.create(db, x_organization_id, t)
            saved += 1
        except Exception:
            pass # Skip errors or duplicates for MVP
    return {"message": f"Successfully imported {saved} transactions."}
