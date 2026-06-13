from pydantic import BaseModel
from typing import List, Dict, Any, Tuple
import re

from app.ai.llm_client import get_llm_client
from app.config import settings

class CategorizationResult(BaseModel):
    category: str
    confidence: float

class Categorizer:
    # Basic rule-based dictionary
    RULES = {
        r'(?i)starbucks|mcdonalds|subway|restaurant|cafe': 'Meals & Entertainment',
        r'(?i)aws|amazon web services|google cloud|gcp|azure|heroku': 'Software Subscriptions',
        r'(?i)uber|lyft|taxi|transit': 'Travel & Transportation',
        r'(?i)walmart|target|office depot|staples': 'Office Supplies',
        r'(?i)payroll|adp|gusto|paychex': 'Payroll',
        r'(?i)verizon|att|t-mobile|comcast': 'Rent & Utilities',
        r'(?i)facebook|fb ads|google ads|linkedin ads': 'Marketing & Advertising',
        r'(?i)stripe|paypal|square': 'Bank Fees & Financial Charges',
        r'(?i)apple|microsoft|adobe|slack|zoom': 'Software Subscriptions',
        r'(?i)delta|united|american airlines|airbnb|hotel': 'Travel & Transportation',
        r'(?i)insurance|state farm|geico|progressive': 'Insurance & Compliance',
        r'(?i)legal|lawyer|accountant|cpa': 'Professional Services'
    }

    def __init__(self):
        self.llm_client = get_llm_client()
        self.mode = settings.AI_CATEGORIZATION_MODE

    async def categorize(self, description: str, amount: float) -> CategorizationResult:
        """
        Categorize a single transaction description.
        Tries rule-based first, falls back to LLM if configured and no rule matches.
        """
        # 1. Rule-based
        for pattern, category in self.RULES.items():
            if re.search(pattern, description):
                return CategorizationResult(category=category, confidence=0.85)
                
        # 2. LLM fallback (if not strictly rule-based)
        if self.mode != "rule_based":
            prompt = f"Categorize the following transaction: '{description}' for amount ${amount}. Return ONLY the category name from this list: Meals & Entertainment, Software Subscriptions, Travel & Transportation, Office Supplies, Payroll, Rent & Utilities, Marketing & Advertising, Bank Fees & Financial Charges, Insurance & Compliance, Professional Services, Uncategorized."
            try:
                response = await self.llm_client.generate(prompt)
                suggested = response.text.strip()
                if suggested:
                    return CategorizationResult(category=suggested, confidence=0.6)
            except Exception:
                pass
                
        # 3. Default
        return CategorizationResult(category="Uncategorized", confidence=0.0)
