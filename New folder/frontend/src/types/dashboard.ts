export interface DashboardSummary {
  totalRevenue: number;
  totalExpenses: number;
  netProfit: number;
  pendingInvoices: number;
  revenueChange: number;
  expenseChange: number;
  profitChange: number;
  invoiceChange: number;
}

export interface ChartDataPoint {
  name: string;
  income: number;
  expenses: number;
  profit?: number;
}

export interface MonthlyTrend {
  month: string;
  revenue: number;
  expenses: number;
  profit: number;
}

export interface CategoryBreakdown {
  name: string;
  value: number;
  color: string;
  percentage: number;
}

export interface RecentActivity {
  id: string;
  type: 'transaction' | 'invoice' | 'receipt' | 'report';
  title: string;
  description: string;
  amount?: number;
  timestamp: string;
  icon: string;
}
