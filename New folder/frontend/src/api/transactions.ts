import apiClient from './client';
import type { Transaction, TransactionFilter, ImportResult, PaginatedResponse } from '../types';

export const transactionsApi = {
  getAll: async (filters?: TransactionFilter, page = 1, pageSize = 25): Promise<PaginatedResponse<Transaction>> => {
    const { data } = await apiClient.get('/transactions', { params: { ...filters, page, pageSize } });
    return data;
  },

  getById: async (id: string): Promise<Transaction> => {
    const { data } = await apiClient.get(`/transactions/${id}`);
    return data;
  },

  create: async (transaction: Partial<Transaction>): Promise<Transaction> => {
    const { data } = await apiClient.post('/transactions', transaction);
    return data;
  },

  update: async (id: string, updates: Partial<Transaction>): Promise<Transaction> => {
    const { data } = await apiClient.patch(`/transactions/${id}`, updates);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/transactions/${id}`);
  },

  bulkDelete: async (ids: string[]): Promise<void> => {
    await apiClient.post('/transactions/bulk-delete', { ids });
  },

  bulkCategorize: async (ids: string[], category: string): Promise<void> => {
    await apiClient.post('/transactions/bulk-categorize', { ids, category });
  },

  importCsv: async (file: File): Promise<ImportResult> => {
    const formData = new FormData();
    formData.append('file', file);
    const { data } = await apiClient.post('/transactions/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return data;
  },
};
