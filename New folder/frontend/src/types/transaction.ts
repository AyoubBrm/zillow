export type TransactionType = 'income' | 'expense';
export type TransactionStatus = 'categorized' | 'uncategorized' | 'review' | 'reconciled';

export interface Transaction {
  id: string;
  date: string;
  description: string;
  merchant: string;
  amount: number;
  type: TransactionType;
  category: string;
  subcategory?: string;
  status: TransactionStatus;
  aiConfidence?: number;
  accountName: string;
  notes?: string;
  receiptUrl?: string;
  tags?: string[];
  createdAt: string;
  updatedAt: string;
}

export interface TransactionFilter {
  search?: string;
  type?: TransactionType | 'all';
  status?: TransactionStatus | 'all';
  category?: string;
  dateFrom?: string;
  dateTo?: string;
  amountMin?: number;
  amountMax?: number;
  sortBy?: 'date' | 'amount' | 'merchant';
  sortOrder?: 'asc' | 'desc';
}

export interface CategorySuggestion {
  category: string;
  confidence: number;
  subcategory?: string;
}

export interface ImportResult {
  totalRows: number;
  imported: number;
  duplicates: number;
  errors: number;
  errorDetails: string[];
}

export interface TransactionSummary {
  totalIncome: number;
  totalExpenses: number;
  netProfit: number;
  transactionCount: number;
}
