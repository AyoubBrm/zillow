import apiClient from './client';

export interface Report {
  id: string;
  type: 'profit_loss' | 'expense' | 'tax_summary' | 'balance_sheet';
  title: string;
  dateFrom: string;
  dateTo: string;
  generatedAt: string;
  data: Record<string, unknown>;
}

export const reportsApi = {
  generate: async (type: string, dateFrom: string, dateTo: string): Promise<Report> => {
    const { data } = await apiClient.post('/reports/generate', { type, dateFrom, dateTo });
    return data;
  },

  getAll: async (): Promise<Report[]> => {
    const { data } = await apiClient.get('/reports');
    return data;
  },

  getById: async (id: string): Promise<Report> => {
    const { data } = await apiClient.get(`/reports/${id}`);
    return data;
  },

  exportCsv: async (id: string): Promise<Blob> => {
    const { data } = await apiClient.get(`/reports/${id}/export/csv`, { responseType: 'blob' });
    return data;
  },

  exportPdf: async (id: string): Promise<Blob> => {
    const { data } = await apiClient.get(`/reports/${id}/export/pdf`, { responseType: 'blob' });
    return data;
  },
};
