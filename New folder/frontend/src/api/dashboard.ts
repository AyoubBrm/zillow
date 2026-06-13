import apiClient from './client';
import type { DashboardSummary, MonthlyTrend, CategoryBreakdown } from '../types';

export const dashboardApi = {
  getSummary: async (): Promise<DashboardSummary> => {
    const { data } = await apiClient.get('/dashboard/summary');
    return data;
  },

  getMonthlyTrends: async (months?: number): Promise<MonthlyTrend[]> => {
    const { data } = await apiClient.get('/dashboard/trends', { params: { months } });
    return data;
  },

  getCategoryBreakdown: async (): Promise<CategoryBreakdown[]> => {
    const { data } = await apiClient.get('/dashboard/categories');
    return data;
  },
};
