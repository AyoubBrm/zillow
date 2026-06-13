from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Dict, Any, List
from datetime import date
from decimal import Decimal

from app.models.transaction import Transaction
from app.models.category import Category
from app.schemas.report import ReportResponse

class ReportService:
    @staticmethod
    async def generate_profit_loss(db: AsyncSession, organization_id: str, start_date: date, end_date: date) -> ReportResponse:
        """
        Generate a Profit and Loss report.
        """
        # We need transactions grouped by category and type
        stmt = select(
            Transaction.type,
            Category.name.label("category_name"),
            func.sum(Transaction.amount).label("total")
        ).outerjoin(
            Transaction.categories # Junction table
        ).outerjoin(
            Category
        ).where(
            and_(
                Transaction.organization_id == organization_id,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            )
        ).group_by(Transaction.type, Category.name)
        
        result = await db.execute(stmt)
        
        income_data = {}
        expense_data = {}
        
        total_income = Decimal('0.0')
        total_expense = Decimal('0.0')
        
        for row in result.all():
            cat_name = row.category_name or "Uncategorized"
            amount = row.total or Decimal('0.0')
            
            if row.type == "income":
                income_data[cat_name] = float(amount)
                total_income += amount
            elif row.type == "expense":
                expense_data[cat_name] = float(amount)
                total_expense += amount
                
        data = {
            "income": income_data,
            "expenses": expense_data,
            "total_income": float(total_income),
            "total_expenses": float(total_expense),
            "net_profit": float(total_income - total_expense)
        }
        
        return ReportResponse(
            id="temp-id",
            organization_id=organization_id,
            type="profit_loss",
            period_start=start_date,
            period_end=end_date,
            data=data,
            status="ready"
        )
