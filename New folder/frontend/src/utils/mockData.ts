import { format, subDays, subMonths } from 'date-fns';
import type { Transaction } from '../types/transaction';
import type { DashboardSummary, ChartDataPoint, CategoryBreakdown, MonthlyTrend } from '../types/dashboard';

// ========================
// MOCK TRANSACTIONS (60+)
// ========================
const merchants = [
  { name: 'Amazon Web Services', category: 'Cloud & Hosting', type: 'expense' as const },
  { name: 'Google Workspace', category: 'Software & SaaS', type: 'expense' as const },
  { name: 'Shopify', category: 'E-commerce Platform', type: 'expense' as const },
  { name: 'Stripe', category: 'Payment Processing', type: 'expense' as const },
  { name: 'Slack Technologies', category: 'Software & SaaS', type: 'expense' as const },
  { name: 'Adobe Creative Cloud', category: 'Software & SaaS', type: 'expense' as const },
  { name: 'WeWork', category: 'Office & Rent', type: 'expense' as const },
  { name: 'Starbucks', category: 'Meals & Entertainment', type: 'expense' as const },
  { name: 'Uber', category: 'Travel & Transport', type: 'expense' as const },
  { name: 'Delta Airlines', category: 'Travel & Transport', type: 'expense' as const },
  { name: 'Figma', category: 'Software & SaaS', type: 'expense' as const },
  { name: 'Notion', category: 'Software & SaaS', type: 'expense' as const },
  { name: 'HubSpot', category: 'Marketing', type: 'expense' as const },
  { name: 'LinkedIn Ads', category: 'Marketing', type: 'expense' as const },
  { name: 'Meta Ads', category: 'Marketing', type: 'expense' as const },
  { name: 'Zoom', category: 'Software & SaaS', type: 'expense' as const },
  { name: 'Comcast Business', category: 'Utilities', type: 'expense' as const },
  { name: 'Gusto Payroll', category: 'Payroll', type: 'expense' as const },
  { name: 'State Farm Insurance', category: 'Insurance', type: 'expense' as const },
  { name: 'Office Depot', category: 'Office Supplies', type: 'expense' as const },
  { name: 'FedEx', category: 'Shipping', type: 'expense' as const },
  { name: 'Acme Corp', category: 'Client Payment', type: 'income' as const },
  { name: 'Globex Industries', category: 'Client Payment', type: 'income' as const },
  { name: 'Initech Solutions', category: 'Client Payment', type: 'income' as const },
  { name: 'Hooli Inc', category: 'Client Payment', type: 'income' as const },
  { name: 'Pied Piper', category: 'Consulting Revenue', type: 'income' as const },
  { name: 'Stark Industries', category: 'Client Payment', type: 'income' as const },
  { name: 'Wayne Enterprises', category: 'Consulting Revenue', type: 'income' as const },
  { name: 'Cyberdyne Systems', category: 'Client Payment', type: 'income' as const },
  { name: 'Wonka Industries', category: 'Product Revenue', type: 'income' as const },
  { name: 'Umbrella Corp', category: 'Client Payment', type: 'income' as const },
  { name: 'Mailchimp', category: 'Marketing', type: 'expense' as const },
  { name: 'Vercel', category: 'Cloud & Hosting', type: 'expense' as const },
  { name: 'GitHub', category: 'Software & SaaS', type: 'expense' as const },
  { name: 'Datadog', category: 'Cloud & Hosting', type: 'expense' as const },
  { name: 'Grubhub', category: 'Meals & Entertainment', type: 'expense' as const },
  { name: 'Hilton Hotels', category: 'Travel & Transport', type: 'expense' as const },
  { name: 'Verizon Business', category: 'Utilities', type: 'expense' as const },
];

const descriptions: Record<string, string[]> = {
  'Cloud & Hosting': ['Monthly server costs', 'CDN bandwidth charges', 'Database hosting fees', 'Cloud storage plan'],
  'Software & SaaS': ['Monthly subscription', 'Annual license renewal', 'Team plan upgrade', 'Pro tier subscription'],
  'Office & Rent': ['Monthly office rent', 'Hot desk allocation', 'Meeting room booking'],
  'Meals & Entertainment': ['Team lunch', 'Client dinner', 'Coffee meeting', 'Team offsite catering'],
  'Travel & Transport': ['Business trip flight', 'Client meeting ride', 'Airport transfer', 'Hotel stay'],
  'Marketing': ['Ad campaign spend', 'Social media promotion', 'Content marketing tools', 'Email campaign'],
  'Utilities': ['Internet service', 'Phone plan', 'Office electricity'],
  'Payroll': ['Monthly payroll processing', 'Payroll processing fee', 'Benefits administration'],
  'Insurance': ['Business liability insurance', 'Workers comp premium', 'Property insurance'],
  'Office Supplies': ['Printer supplies', 'Desk accessories', 'Ergonomic equipment'],
  'Shipping': ['Client deliverable shipping', 'Package delivery', 'Express shipment'],
  'Client Payment': ['Project milestone payment', 'Retainer payment', 'Final project delivery', 'Monthly retainer'],
  'Consulting Revenue': ['Consulting engagement', 'Advisory session', 'Strategic consultation'],
  'Product Revenue': ['Product license sale', 'Subscription revenue', 'Product sale'],
  'Payment Processing': ['Transaction processing fees', 'Monthly processing', 'Platform fees'],
  'E-commerce Platform': ['Monthly platform fee', 'Transaction fee', 'App subscription'],
};

const statuses: ('categorized' | 'uncategorized' | 'review' | 'reconciled')[] = ['categorized', 'categorized', 'categorized', 'reconciled', 'reconciled', 'review', 'uncategorized'];

function randomBetween(min: number, max: number): number {
  return Math.round((Math.random() * (max - min) + min) * 100) / 100;
}

function generateTransactions(): Transaction[] {
  const transactions: Transaction[] = [];
  const now = new Date();

  for (let i = 0; i < 65; i++) {
    const merchant = merchants[i % merchants.length];
    const daysAgo = Math.floor(Math.random() * 180);
    const date = subDays(now, daysAgo);
    const descList = descriptions[merchant.category] || ['Payment'];
    const desc = descList[Math.floor(Math.random() * descList.length)];

    let amount: number;
    if (merchant.type === 'income') {
      amount = randomBetween(2500, 35000);
    } else {
      switch (merchant.category) {
        case 'Payroll': amount = randomBetween(8000, 25000); break;
        case 'Office & Rent': amount = randomBetween(2000, 5500); break;
        case 'Cloud & Hosting': amount = randomBetween(150, 2500); break;
        case 'Software & SaaS': amount = randomBetween(15, 499); break;
        case 'Marketing': amount = randomBetween(500, 5000); break;
        case 'Travel & Transport': amount = randomBetween(50, 3000); break;
        case 'Insurance': amount = randomBetween(300, 1500); break;
        default: amount = randomBetween(10, 500);
      }
    }

    transactions.push({
      id: `txn_${String(i + 1).padStart(4, '0')}`,
      date: format(date, 'yyyy-MM-dd'),
      description: `${desc} — ${merchant.name}`,
      merchant: merchant.name,
      amount,
      type: merchant.type,
      category: merchant.category,
      status: statuses[Math.floor(Math.random() * statuses.length)],
      aiConfidence: merchant.type === 'income' ? randomBetween(0.92, 0.99) : randomBetween(0.78, 0.99),
      accountName: 'Chase Business Checking',
      tags: [],
      createdAt: date.toISOString(),
      updatedAt: date.toISOString(),
    });
  }

  return transactions.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
}

export const mockTransactions: Transaction[] = generateTransactions();

// ========================
// DASHBOARD SUMMARY
// ========================
export const mockDashboardSummary: DashboardSummary = {
  totalRevenue: 284750.00,
  totalExpenses: 156320.00,
  netProfit: 128430.00,
  pendingInvoices: 12,
  revenueChange: 12.5,
  expenseChange: -3.2,
  profitChange: 24.8,
  invoiceChange: -8.3,
};

// ========================
// MONTHLY CHART DATA
// ========================
export function generateMonthlyData(): ChartDataPoint[] {
  const now = new Date();
  const data: ChartDataPoint[] = [];

  for (let i = 11; i >= 0; i--) {
    const date = subMonths(now, i);
    const monthName = format(date, 'MMM yyyy');
    const income = randomBetween(18000, 35000);
    const expenses = randomBetween(10000, 22000);

    data.push({
      name: monthName,
      income,
      expenses,
      profit: income - expenses,
    });
  }

  return data;
}

export const mockChartData: ChartDataPoint[] = [
  { name: 'Jul 2025', income: 22400, expenses: 14200, profit: 8200 },
  { name: 'Aug 2025', income: 24800, expenses: 15100, profit: 9700 },
  { name: 'Sep 2025', income: 21500, expenses: 13800, profit: 7700 },
  { name: 'Oct 2025', income: 27600, expenses: 16400, profit: 11200 },
  { name: 'Nov 2025', income: 25200, expenses: 14900, profit: 10300 },
  { name: 'Dec 2025', income: 23100, expenses: 17200, profit: 5900 },
  { name: 'Jan 2026', income: 19800, expenses: 13100, profit: 6700 },
  { name: 'Feb 2026', income: 26400, expenses: 14700, profit: 11700 },
  { name: 'Mar 2026', income: 28900, expenses: 15800, profit: 13100 },
  { name: 'Apr 2026', income: 31200, expenses: 16200, profit: 15000 },
  { name: 'May 2026', income: 29400, expenses: 14400, profit: 15000 },
  { name: 'Jun 2026', income: 33500, expenses: 15600, profit: 17900 },
];

// ========================
// CATEGORY BREAKDOWN
// ========================
export const mockCategoryBreakdown: CategoryBreakdown[] = [
  { name: 'Payroll', value: 52000, color: '#8b5cf6', percentage: 33.2 },
  { name: 'Cloud & Hosting', value: 18500, color: '#6366f1', percentage: 11.8 },
  { name: 'Marketing', value: 22400, color: '#f43f5e', percentage: 14.3 },
  { name: 'Software & SaaS', value: 12800, color: '#10b981', percentage: 8.2 },
  { name: 'Office & Rent', value: 16500, color: '#f59e0b', percentage: 10.5 },
  { name: 'Travel & Transport', value: 14200, color: '#3b82f6', percentage: 9.1 },
  { name: 'Meals & Entertainment', value: 4800, color: '#ec4899', percentage: 3.1 },
  { name: 'Other', value: 15120, color: '#64748b', percentage: 9.7 },
];

// ========================
// MONTHLY TRENDS
// ========================
export const mockMonthlyTrends: MonthlyTrend[] = [
  { month: 'Jul 2025', revenue: 22400, expenses: 14200, profit: 8200 },
  { month: 'Aug 2025', revenue: 24800, expenses: 15100, profit: 9700 },
  { month: 'Sep 2025', revenue: 21500, expenses: 13800, profit: 7700 },
  { month: 'Oct 2025', revenue: 27600, expenses: 16400, profit: 11200 },
  { month: 'Nov 2025', revenue: 25200, expenses: 14900, profit: 10300 },
  { month: 'Dec 2025', revenue: 23100, expenses: 17200, profit: 5900 },
  { month: 'Jan 2026', revenue: 19800, expenses: 13100, profit: 6700 },
  { month: 'Feb 2026', revenue: 26400, expenses: 14700, profit: 11700 },
  { month: 'Mar 2026', revenue: 28900, expenses: 15800, profit: 13100 },
  { month: 'Apr 2026', revenue: 31200, expenses: 16200, profit: 15000 },
  { month: 'May 2026', revenue: 29400, expenses: 14400, profit: 15000 },
  { month: 'Jun 2026', revenue: 33500, expenses: 15600, profit: 17900 },
];

// ========================
// FORMAT HELPERS
// ========================
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

export function formatCurrencyFull(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
}

export function formatPercentage(value: number): string {
  return `${value >= 0 ? '+' : ''}${value.toFixed(1)}%`;
}

export function formatCompactNumber(value: number): string {
  if (value >= 1000000) return `$${(value / 1000000).toFixed(1)}M`;
  if (value >= 1000) return `$${(value / 1000).toFixed(1)}K`;
  return `$${value}`;
}
