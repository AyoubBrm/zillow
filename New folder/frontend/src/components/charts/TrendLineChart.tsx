import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { mockMonthlyTrends, formatCurrency } from '../../utils/mockData';
import type { MonthlyTrend } from '../../types/dashboard';

interface TrendLineChartProps {
  data?: MonthlyTrend[];
}

const CustomTooltip: React.FC<{ active?: boolean; payload?: Array<{ value: number; dataKey: string; color: string }>; label?: string }> = ({
  active,
  payload,
  label,
}) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-slate-900/95 backdrop-blur-xl border border-white/10 rounded-xl p-4 shadow-xl min-w-[180px]">
        <p className="text-xs text-slate-400 mb-2 font-medium">{label}</p>
        {payload.map((entry, index) => (
          <div key={index} className="flex items-center justify-between gap-4 mb-1">
            <div className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: entry.color }} />
              <span className="text-xs text-slate-300 capitalize">{entry.dataKey}</span>
            </div>
            <span className="text-xs font-semibold text-slate-100">{formatCurrency(entry.value)}</span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

const TrendLineChart: React.FC<TrendLineChartProps> = ({ data = mockMonthlyTrends }) => {
  return (
    <ResponsiveContainer width="100%" height={320}>
      <LineChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
        <XAxis
          dataKey="month"
          tick={{ fill: '#64748b', fontSize: 12 }}
          tickLine={false}
          axisLine={{ stroke: 'rgba(255,255,255,0.05)' }}
        />
        <YAxis
          tick={{ fill: '#64748b', fontSize: 12 }}
          tickLine={false}
          axisLine={false}
          tickFormatter={(value: number) => `$${(value / 1000).toFixed(0)}K`}
        />
        <Tooltip content={<CustomTooltip />} />
        <Legend
          verticalAlign="top"
          height={36}
          iconType="circle"
          iconSize={8}
          formatter={(value: string) => (
            <span className="text-xs text-slate-400 capitalize">{value}</span>
          )}
        />
        <Line
          type="monotone"
          dataKey="revenue"
          stroke="#10b981"
          strokeWidth={2.5}
          dot={false}
          activeDot={{ r: 5, fill: '#10b981', stroke: '#0a0e1a', strokeWidth: 2 }}
        />
        <Line
          type="monotone"
          dataKey="expenses"
          stroke="#f43f5e"
          strokeWidth={2.5}
          dot={false}
          activeDot={{ r: 5, fill: '#f43f5e', stroke: '#0a0e1a', strokeWidth: 2 }}
        />
        <Line
          type="monotone"
          dataKey="profit"
          stroke="#8b5cf6"
          strokeWidth={2.5}
          dot={false}
          strokeDasharray="5 5"
          activeDot={{ r: 5, fill: '#8b5cf6', stroke: '#0a0e1a', strokeWidth: 2 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default TrendLineChart;
