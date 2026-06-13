import React from 'react';
import { TrendingUp, TrendingDown, DollarSign, FileText } from 'lucide-react';
import RevenueChart from '../../components/charts/RevenueChart';
import ExpenseChart from '../../components/charts/ExpenseChart';
import CategoryPieChart from '../../components/charts/CategoryPieChart';

const DashboardPage = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-white">Dashboard Overview</h1>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="glass-card p-6 rounded-xl border border-white/5">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-slate-400 text-sm font-medium">Total Revenue</p>
              <h3 className="text-3xl font-bold text-white mt-2">$24,500</h3>
            </div>
            <div className="p-3 bg-emerald-500/10 rounded-lg">
              <TrendingUp className="text-emerald-500 w-6 h-6" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <span className="text-emerald-400 font-medium">+12.5%</span>
            <span className="text-slate-500 ml-2">vs last month</span>
          </div>
        </div>

        <div className="glass-card p-6 rounded-xl border border-white/5">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-slate-400 text-sm font-medium">Total Expenses</p>
              <h3 className="text-3xl font-bold text-white mt-2">$8,240</h3>
            </div>
            <div className="p-3 bg-rose-500/10 rounded-lg">
              <TrendingDown className="text-rose-500 w-6 h-6" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <span className="text-rose-400 font-medium">-4.2%</span>
            <span className="text-slate-500 ml-2">vs last month</span>
          </div>
        </div>

        <div className="glass-card p-6 rounded-xl border border-white/5">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-slate-400 text-sm font-medium">Net Profit</p>
              <h3 className="text-3xl font-bold text-white mt-2">$16,260</h3>
            </div>
            <div className="p-3 bg-violet-500/10 rounded-lg">
              <DollarSign className="text-violet-500 w-6 h-6" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <span className="text-emerald-400 font-medium">+18.2%</span>
            <span className="text-slate-500 ml-2">vs last month</span>
          </div>
        </div>

        <div className="glass-card p-6 rounded-xl border border-white/5">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-slate-400 text-sm font-medium">Pending Invoices</p>
              <h3 className="text-3xl font-bold text-white mt-2">4</h3>
            </div>
            <div className="p-3 bg-amber-500/10 rounded-lg">
              <FileText className="text-amber-500 w-6 h-6" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <span className="text-slate-400 font-medium">$3,400 awaiting payment</span>
          </div>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-card p-6 rounded-xl border border-white/5">
          <h3 className="text-lg font-medium text-white mb-4">Revenue Trend</h3>
          <div className="h-72">
            <RevenueChart />
          </div>
        </div>
        <div className="glass-card p-6 rounded-xl border border-white/5">
          <h3 className="text-lg font-medium text-white mb-4">Expense Breakdown</h3>
          <div className="h-72">
            <CategoryPieChart />
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
