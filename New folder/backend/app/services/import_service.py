import pandas as pd
from typing import List, Dict, Any, BinaryIO
import io
import hashlib
from app.schemas.transaction import TransactionCreate

class ImportService:
    @staticmethod
    async def parse_file(file_content: bytes, filename: str, organization_id: str, account_id: str) -> List[TransactionCreate]:
        """
        Parse CSV or Excel file and return a list of TransactionCreate schemas.
        """
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(file_content))
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(io.BytesIO(file_content))
        else:
            raise ValueError("Unsupported file format. Please upload CSV or Excel.")

        # Try to standardize column names
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        # Expected columns: date, description, amount
        # Map common variations
        col_mapping = {
            'date': 'date', 'transaction date': 'date', 'posted date': 'date',
            'description': 'description', 'memo': 'description', 'payee': 'description', 'name': 'description',
            'amount': 'amount', 'value': 'amount'
        }
        
        mapped_df = pd.DataFrame()
        for col in df.columns:
            if col in col_mapping:
                mapped_df[col_mapping[col]] = df[col]
                
        if not all(required in mapped_df.columns for required in ['date', 'description', 'amount']):
            raise ValueError("File must contain Date, Description, and Amount columns.")
            
        transactions = []
        for _, row in mapped_df.iterrows():
            try:
                date_val = pd.to_datetime(row['date']).date()
                amount_val = float(row['amount'])
                description_val = str(row['description']).strip()
                
                # Simple duplicate hash: date + amount + desc
                hash_str = f"{date_val}{amount_val}{description_val}".encode('utf-8')
                fingerprint = hashlib.sha256(hash_str).hexdigest()
                
                t = TransactionCreate(
                    bank_account_id=account_id,
                    amount=abs(amount_val),
                    currency="USD",
                    description=description_val,
                    merchant_name=description_val, # Basic assumption, AI categorizer can refine
                    transaction_date=date_val,
                    type="income" if amount_val > 0 else "expense",
                    source="csv_import",
                    status="pending",
                    hash_fingerprint=fingerprint
                )
                transactions.append(t)
            except Exception as e:
                # Skip rows that fail parsing
                continue
                
        return transactions
