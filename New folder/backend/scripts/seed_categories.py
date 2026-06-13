import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import async_session
from app.models.category import Category

DEFAULT_CATEGORIES = [
    # Income
    {"name": "Sales Revenue", "type": "income", "is_system": True},
    {"name": "Service Revenue", "type": "income", "is_system": True},
    {"name": "Interest Income", "type": "income", "is_system": True},
    {"name": "Other Income", "type": "income", "is_system": True},
    
    # Expenses
    {"name": "Meals & Entertainment", "type": "expense", "is_system": True},
    {"name": "Software Subscriptions", "type": "expense", "is_system": True},
    {"name": "Travel & Transportation", "type": "expense", "is_system": True},
    {"name": "Office Supplies", "type": "expense", "is_system": True},
    {"name": "Payroll", "type": "expense", "is_system": True},
    {"name": "Rent & Utilities", "type": "expense", "is_system": True},
    {"name": "Marketing & Advertising", "type": "expense", "is_system": True},
    {"name": "Bank Fees & Financial Charges", "type": "expense", "is_system": True},
    {"name": "Insurance & Compliance", "type": "expense", "is_system": True},
    {"name": "Professional Services", "type": "expense", "is_system": True},
    {"name": "Cost of Goods Sold (COGS)", "type": "expense", "is_system": True},
    {"name": "Depreciation", "type": "expense", "is_system": True},
    
    # Special
    {"name": "Uncategorized", "type": "expense", "is_system": True},
    {"name": "Transfer", "type": "transfer", "is_system": True},
]

async def seed_categories():
    async with async_session() as session:
        for cat_data in DEFAULT_CATEGORIES:
            # Check if exists
            stmt = select(Category).where(
                Category.name == cat_data["name"],
                Category.organization_id == None
            )
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if not existing:
                category = Category(
                    name=cat_data["name"],
                    type=cat_data["type"],
                    is_system=True
                )
                session.add(category)
        
        await session.commit()
        print("✅ Default categories seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed_categories())
