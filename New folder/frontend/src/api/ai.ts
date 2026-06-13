import apiClient from './client';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export const aiApi = {
  chat: async (message: string): Promise<ChatMessage> => {
    const { data } = await apiClient.post('/ai/chat', { message });
    return data;
  },

  categorize: async (transactionId: string): Promise<{ category: string; confidence: number }> => {
    const { data } = await apiClient.post('/ai/categorize', { transactionId });
    return data;
  },

  generateInsights: async (): Promise<{ insights: string[] }> => {
    const { data } = await apiClient.get('/ai/insights');
    return data;
  },
};
