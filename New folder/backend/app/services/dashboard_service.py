from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, extract
from typing import Dict, Any, List
from datetime import date, timedelta
import datetime

from app.models.transaction import Transaction
from app.models.category import Category
from app.schemas.dashboard import DashboardSummary, ChartDataPoint, MonthlyTrend

class DashboardService:
    @staticmethod
    async def get_summary(db: AsyncSession, organization_id: str) -> DashboardSummary:
        today = date.today()
        first_day_current_month = today.replace(day=1)
        last_day_prev_month = first_day_current_month - timedelta(days=1)
        first_day_prev_month = last_day_prev_month.replace(day=1)

        # Get current month totals
        stmt_current = select(
            func.sum(Transaction.amount).label("total"),
            Transaction.type
        ).where(
            and_(
                Transaction.organization_id == organization_id,
                Transaction.transaction_date >= first_day_current_month,
                Transaction.transaction_date <= today
            )
        ).group_by(Transaction.type)
        
        result_current = await db.execute(stmt_current)
        current_data = {row.type: row.total or 0.0 for row in result_current.all()}
        current_income = float(current_data.get("income", 0.0))
        current_expense = float(current_data.get("expense", 0.0))

        # Get previous month totals for % change calculation
        stmt_prev = select(
            func.sum(Transaction.amount).label("total"),
            Transaction.type
        ).where(
            and_(
                Transaction.organization_id == organization_id,
                Transaction.transaction_date >= first_day_prev_month,
                Transaction.transaction_date <= last_day_prev_month
            )
        ).group_by(Transaction.type)
        
        result_prev = await db.execute(stmt_prev)
        prev_data = {row.type: row.total or 0.0 for row in result_prev.all()}
        prev_income = float(prev_data.get("income", 0.0))
        prev_expense = float(prev_data.get("expense", 0.0))
        
        # Calculate % changes safely
        income_change = ((current_income - prev_income) / prev_income * 100) if prev_income else 0.0
        expense_change = ((current_expense - prev_expense) / prev_expense * 100) if prev_expense else 0.0
        
        current_profit = current_income - current_expense
        prev_profit = prev_income - prev_expense
        profit_change = ((current_profit - prev_profit) / abs(prev_profit) * 100) if prev_profit else 0.0

        return DashboardSummary(
            total_revenue=current_income,
            revenue_change=income_change,
            total_expenses=current_expense,
            expenses_change=expense_change,
            net_profit=current_profit,
            profit_change=profit_change,
            pending_invoices=0, # Placeholder
            invoices_change=0.0
        )

    @staticmethod
    async def get_monthly_trends(db: AsyncSession, organization_id: str, months: int = 6) -> List[MonthlyTrend]:
        # Calculate 6 months ago
        start_date = (date.today().replace(day=1) - timedelta(days=30 * months)).replace(day=1)
        
        stmt = select(
            func.date_trunc('month', Transaction.transaction_date).label('month'),
            Transaction.type,
            func.sum(Transaction.amount).label('total')
        ).where(
            and_(
                Transaction.organization_id == organization_id,
                Transaction.transaction_date >= start_date
            )
        ).group_by('month', Transaction.type).order_by('month')
        
        result = await db.execute(stmt)
        
        trends_map: Dict[str, MonthlyTrend] = {}
        for row in result.all():
            month_str = row.month.strftime("%b %Y")
            if month_str not in trends_map:
                trends_map[month_str] = MonthlyTrend(month=month_str, revenue=0.0, expenses=0.0, profit=0.0)
            
            if row.type == "income":
                trends_map[month_str].revenue = float(row.total or 0.0)
            elif row.type == "expense":
                trends_map[month_str].expenses = float(row.total or 0.0)
                
            trends_map[month_str].profit = trends_map[month_str].revenue - trends_map[month_str].expenses
            
        return list(trends_map.values())
