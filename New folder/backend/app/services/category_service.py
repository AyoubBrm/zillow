"""Category service — CRUD and default category seeding."""

from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictException, NotFoundException
from app.models.category import Category, CategoryType
from app.repositories.category_repo import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    """Business logic for accounting categories."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = CategoryRepository(session)

    async def create_category(
        self, org_id: UUID, payload: CategoryCreate
    ) -> Category:
        """Create a new category for the organisation."""
        existing = await self.repo.get_by_name(payload.name, org_id)
        if existing is not None:
            raise ConflictException(f"Category '{payload.name}' already exists.")

        data = payload.model_dump()
        data["organization_id"] = org_id
        data["is_system"] = False
        return await self.repo.create(data)

    async def get_category(self, category_id: UUID, org_id: UUID) -> Category:
        """Fetch a category by ID."""
        cat = await self.repo.get(category_id)
        if cat is None:
            raise NotFoundException("Category not found.")
        # Ensure org access
        if cat.organization_id is not None and cat.organization_id != org_id:
            raise NotFoundException("Category not found.")
        return cat

    async def list_categories(
        self, org_id: UUID, *, include_system: bool = True
    ) -> Sequence[Category]:
        """Return all categories visible to the organisation."""
        return await self.repo.get_for_org(org_id, include_system=include_system)

    async def get_tree(self, org_id: UUID) -> Sequence[Category]:
        """Return root-level categories (children loaded via relationship)."""
        return await self.repo.get_roots(org_id)

    async def update_category(
        self, org_id: UUID, category_id: UUID, payload: CategoryUpdate
    ) -> Category:
        """Update a category (only org-owned categories, not system ones)."""
        cat = await self.get_category(category_id, org_id)
        if cat.is_system:
            raise ConflictException("System categories cannot be modified.")
        data = payload.model_dump(exclude_unset=True)
        updated = await self.repo.update(category_id, data)
        if updated is None:
            raise NotFoundException("Category not found.")
        return updated

    async def delete_category(self, org_id: UUID, category_id: UUID) -> bool:
        """Delete a category (only org-owned)."""
        cat = await self.get_category(category_id, org_id)
        if cat.is_system:
            raise ConflictException("System categories cannot be deleted.")
        return await self.repo.delete(category_id)

    async def seed_defaults(self) -> int:
        """Seed the system with default accounting categories.

        Returns the number of categories created.  Skips if already seeded.
        """
        if await self.repo.system_categories_exist():
            return 0

        created = 0
        for idx, (name, cat_type, code, parent_name) in enumerate(DEFAULT_CATEGORIES):
            parent_id = None
            if parent_name:
                parent = await self.repo.get_by_name(parent_name)
                if parent:
                    parent_id = parent.id
            await self.repo.create({
                "name": name,
                "code": code,
                "type": cat_type,
                "parent_id": parent_id,
                "is_system": True,
                "is_active": True,
                "sort_order": idx,
            })
            created += 1

        return created


# ── Default categories (50+ real accounting categories) ──────────────────────

DEFAULT_CATEGORIES: list[tuple[str, CategoryType, str, str | None]] = [
    # === Income ===
    ("Revenue", CategoryType.INCOME, "4000", None),
    ("Sales Revenue", CategoryType.INCOME, "4010", "Revenue"),
    ("Service Revenue", CategoryType.INCOME, "4020", "Revenue"),
    ("Consulting Income", CategoryType.INCOME, "4030", "Revenue"),
    ("Subscription Revenue", CategoryType.INCOME, "4040", "Revenue"),
    ("Interest Income", CategoryType.INCOME, "4050", "Revenue"),
    ("Dividend Income", CategoryType.INCOME, "4060", "Revenue"),
    ("Rental Income", CategoryType.INCOME, "4070", "Revenue"),
    ("Commission Income", CategoryType.INCOME, "4080", "Revenue"),
    ("Refunds Received", CategoryType.INCOME, "4090", "Revenue"),
    ("Other Income", CategoryType.INCOME, "4100", "Revenue"),

    # === Expenses ===
    ("Operating Expenses", CategoryType.EXPENSE, "5000", None),

    # Payroll
    ("Payroll", CategoryType.EXPENSE, "5100", "Operating Expenses"),
    ("Salaries & Wages", CategoryType.EXPENSE, "5110", "Payroll"),
    ("Employee Benefits", CategoryType.EXPENSE, "5120", "Payroll"),
    ("Payroll Taxes", CategoryType.EXPENSE, "5130", "Payroll"),
    ("Contractor Payments", CategoryType.EXPENSE, "5140", "Payroll"),

    # Facilities
    ("Facilities", CategoryType.EXPENSE, "5200", "Operating Expenses"),
    ("Rent", CategoryType.EXPENSE, "5210", "Facilities"),
    ("Utilities", CategoryType.EXPENSE, "5220", "Facilities"),
    ("Office Supplies", CategoryType.EXPENSE, "5230", "Facilities"),
    ("Maintenance & Repairs", CategoryType.EXPENSE, "5240", "Facilities"),
    ("Cleaning Services", CategoryType.EXPENSE, "5250", "Facilities"),

    # Technology
    ("Technology", CategoryType.EXPENSE, "5300", "Operating Expenses"),
    ("Software & SaaS", CategoryType.EXPENSE, "5310", "Technology"),
    ("Hardware & Equipment", CategoryType.EXPENSE, "5320", "Technology"),
    ("Cloud Services", CategoryType.EXPENSE, "5330", "Technology"),
    ("Domain & Hosting", CategoryType.EXPENSE, "5340", "Technology"),
    ("IT Support", CategoryType.EXPENSE, "5350", "Technology"),

    # Marketing
    ("Marketing & Advertising", CategoryType.EXPENSE, "5400", "Operating Expenses"),
    ("Online Advertising", CategoryType.EXPENSE, "5410", "Marketing & Advertising"),
    ("Print Advertising", CategoryType.EXPENSE, "5420", "Marketing & Advertising"),
    ("Social Media Marketing", CategoryType.EXPENSE, "5430", "Marketing & Advertising"),
    ("Events & Sponsorships", CategoryType.EXPENSE, "5440", "Marketing & Advertising"),
    ("Marketing Materials", CategoryType.EXPENSE, "5450", "Marketing & Advertising"),

    # Travel & Entertainment
    ("Travel & Entertainment", CategoryType.EXPENSE, "5500", "Operating Expenses"),
    ("Airfare", CategoryType.EXPENSE, "5510", "Travel & Entertainment"),
    ("Hotels & Lodging", CategoryType.EXPENSE, "5520", "Travel & Entertainment"),
    ("Meals & Entertainment", CategoryType.EXPENSE, "5530", "Travel & Entertainment"),
    ("Ground Transportation", CategoryType.EXPENSE, "5540", "Travel & Entertainment"),
    ("Parking & Tolls", CategoryType.EXPENSE, "5550", "Travel & Entertainment"),

    # Professional Services
    ("Professional Services", CategoryType.EXPENSE, "5600", "Operating Expenses"),
    ("Legal Fees", CategoryType.EXPENSE, "5610", "Professional Services"),
    ("Accounting Fees", CategoryType.EXPENSE, "5620", "Professional Services"),
    ("Consulting Fees", CategoryType.EXPENSE, "5630", "Professional Services"),

    # Insurance
    ("Insurance", CategoryType.EXPENSE, "5700", "Operating Expenses"),
    ("General Liability Insurance", CategoryType.EXPENSE, "5710", "Insurance"),
    ("Professional Liability Insurance", CategoryType.EXPENSE, "5720", "Insurance"),
    ("Health Insurance", CategoryType.EXPENSE, "5730", "Insurance"),

    # Taxes & Licenses
    ("Taxes & Licenses", CategoryType.EXPENSE, "5800", "Operating Expenses"),
    ("Business Taxes", CategoryType.EXPENSE, "5810", "Taxes & Licenses"),
    ("Licenses & Permits", CategoryType.EXPENSE, "5820", "Taxes & Licenses"),

    # Financial
    ("Financial Charges", CategoryType.EXPENSE, "5900", "Operating Expenses"),
    ("Bank Fees", CategoryType.EXPENSE, "5910", "Financial Charges"),
    ("Credit Card Processing", CategoryType.EXPENSE, "5920", "Financial Charges"),
    ("Interest Expense", CategoryType.EXPENSE, "5930", "Financial Charges"),
    ("Late Payment Fees", CategoryType.EXPENSE, "5940", "Financial Charges"),

    # Other
    ("Shipping & Postage", CategoryType.EXPENSE, "6100", "Operating Expenses"),
    ("Subscriptions & Memberships", CategoryType.EXPENSE, "6200", "Operating Expenses"),
    ("Training & Education", CategoryType.EXPENSE, "6300", "Operating Expenses"),
    ("Depreciation", CategoryType.EXPENSE, "6400", "Operating Expenses"),
    ("Miscellaneous Expenses", CategoryType.EXPENSE, "6500", "Operating Expenses"),

    # === Assets ===
    ("Assets", CategoryType.ASSET, "1000", None),
    ("Cash & Bank Accounts", CategoryType.ASSET, "1100", "Assets"),
    ("Accounts Receivable", CategoryType.ASSET, "1200", "Assets"),
    ("Inventory", CategoryType.ASSET, "1300", "Assets"),
    ("Prepaid Expenses", CategoryType.ASSET, "1400", "Assets"),
    ("Fixed Assets", CategoryType.ASSET, "1500", "Assets"),

    # === Liabilities ===
    ("Liabilities", CategoryType.LIABILITY, "2000", None),
    ("Accounts Payable", CategoryType.LIABILITY, "2100", "Liabilities"),
    ("Credit Cards Payable", CategoryType.LIABILITY, "2200", "Liabilities"),
    ("Accrued Expenses", CategoryType.LIABILITY, "2300", "Liabilities"),
    ("Loans Payable", CategoryType.LIABILITY, "2400", "Liabilities"),
    ("Taxes Payable", CategoryType.LIABILITY, "2500", "Liabilities"),

    # === Equity ===
    ("Equity", CategoryType.EQUITY, "3000", None),
    ("Owner's Equity", CategoryType.EQUITY, "3100", "Equity"),
    ("Retained Earnings", CategoryType.EQUITY, "3200", "Equity"),
    ("Owner's Draw", CategoryType.EQUITY, "3300", "Equity"),
]
