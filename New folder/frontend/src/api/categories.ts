import apiClient from './client';

export interface Category {
  id: string;
  name: string;
  type: 'income' | 'expense';
  color: string;
  icon: string;
  subcategories: string[];
}

export const categoriesApi = {
  getAll: async (): Promise<Category[]> => {
    const { data } = await apiClient.get('/categories');
    return data;
  },

  create: async (category: Partial<Category>): Promise<Category> => {
    const { data } = await apiClient.post('/categories', category);
    return data;
  },

  update: async (id: string, updates: Partial<Category>): Promise<Category> => {
    const { data } = await apiClient.patch(`/categories/${id}`, updates);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/categories/${id}`);
  },
};
