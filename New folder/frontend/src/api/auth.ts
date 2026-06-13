import apiClient from './client';
import type { LoginCredentials, RegisterData, AuthTokens, User } from '../types';

export const authApi = {
  login: async (credentials: LoginCredentials): Promise<{ user: User; tokens: AuthTokens }> => {
    const { data } = await apiClient.post('/auth/login', credentials);
    return data;
  },

  register: async (registerData: RegisterData): Promise<{ user: User; tokens: AuthTokens }> => {
    const { data } = await apiClient.post('/auth/register', registerData);
    return data;
  },

  refreshToken: async (refreshToken: string): Promise<AuthTokens> => {
    const { data } = await apiClient.post('/auth/refresh', { refreshToken });
    return data;
  },

  getProfile: async (): Promise<User> => {
    const { data } = await apiClient.get('/auth/profile');
    return data;
  },

  updateProfile: async (updates: Partial<User>): Promise<User> => {
    const { data } = await apiClient.patch('/auth/profile', updates);
    return data;
  },

  changePassword: async (currentPassword: string, newPassword: string): Promise<void> => {
    await apiClient.post('/auth/change-password', { currentPassword, newPassword });
  },
};
