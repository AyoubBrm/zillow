from fastapi import APIRouter

router = APIRouter()

@router.get("/plans")
async def list_plans():
    return [
        {"id": "free", "name": "Free", "price": 0, "features": ["Basic categorization"]},
        {"id": "starter", "name": "Starter", "price": 19, "features": ["CSV import", "Reports"]},
        {"id": "pro", "name": "Professional", "price": 49, "features": ["AI assistant", "Automations"]}
    ]
