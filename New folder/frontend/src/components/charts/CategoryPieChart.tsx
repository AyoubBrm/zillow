import React from 'react';
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { mockCategoryBreakdown, formatCurrency } from '../../utils/mockData';
import type { CategoryBreakdown } from '../../types/dashboard';

interface CategoryPieChartProps {
  data?: CategoryBreakdown[];
}

const CustomTooltip: React.FC<{ active?: boolean; payload?: Array<{ payload: CategoryBreakdown }> }> = ({
  active,
  payload,
}) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="bg-slate-900/95 backdrop-blur-xl border border-white/10 rounded-xl p-3 shadow-xl">
        <div className="flex items-center gap-2 mb-1">
          <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: data.color }} />
          <span className="text-xs font-medium text-slate-200">{data.name}</span>
        </div>
        <p className="text-sm font-semibold text-slate-100">{formatCurrency(data.value)}</p>
        <p className="text-xs text-slate-400">{data.percentage}% of total</p>
      </div>
    );
  }
  return null;
};

const CategoryPieChart: React.FC<CategoryPieChartProps> = ({ data = mockCategoryBreakdown }) => {
  const total = data.reduce((sum, item) => sum + item.value, 0);

  return (
    <div className="flex flex-col items-center">
      <ResponsiveContainer width="100%" height={240}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={70}
            outerRadius={100}
            paddingAngle={3}
            dataKey="value"
            strokeWidth={0}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} className="transition-opacity duration-200 hover:opacity-80" />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          {/* Center text */}
          <text x="50%" y="47%" textAnchor="middle" className="fill-slate-300 text-xs">
            Total
          </text>
          <text x="50%" y="57%" textAnchor="middle" className="fill-white font-semibold text-sm">
            {formatCurrency(total)}
          </text>
        </PieChart>
      </ResponsiveContainer>

      {/* Legend */}
      <div className="grid grid-cols-2 gap-x-6 gap-y-2 mt-2 w-full">
        {data.map((item) => (
          <div key={item.name} className="flex items-center gap-2 min-w-0">
            <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: item.color }} />
            <span className="text-xs text-slate-400 truncate">{item.name}</span>
            <span className="text-xs text-slate-300 font-medium ml-auto flex-shrink-0">{item.percentage}%</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CategoryPieChart;
