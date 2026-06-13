import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User, AuthTokens } from '../types/auth';

interface AuthStore {
  user: User | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (data: { firstName: string; lastName: string; email: string; password: string; organizationName: string }) => Promise<void>;
  logout: () => void;
  setUser: (user: User) => void;
  setLoading: (loading: boolean) => void;
  clearError: () => void;
}

// Mock user for demo purposes
const mockUser: User = {
  id: 'usr_1a2b3c4d',
  email: 'alex@ledgerai.com',
  firstName: 'Alex',
  lastName: 'Morgan',
  role: 'owner',
  organizationId: 'org_5e6f7g8h',
  organizationName: 'Morgan & Associates LLC',
  createdAt: '2024-01-15T10:00:00Z',
  lastLogin: new Date().toISOString(),
};

const mockTokens: AuthTokens = {
  accessToken: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.mock-access-token',
  refreshToken: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.mock-refresh-token',
};

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      user: null,
      tokens: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (email: string, _password: string) => {
        set({ isLoading: true, error: null });
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1200));

        if (email === 'demo@ledgerai.com' || email === 'alex@ledgerai.com') {
          set({
            user: { ...mockUser, email },
            tokens: mockTokens,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } else {
          // Accept any email for demo
          set({
            user: { ...mockUser, email },
            tokens: mockTokens,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        }
      },

      register: async (data) => {
        set({ isLoading: true, error: null });
        await new Promise(resolve => setTimeout(resolve, 1500));
        set({
          user: {
            ...mockUser,
            email: data.email,
            firstName: data.firstName,
            lastName: data.lastName,
            organizationName: data.organizationName,
          },
          tokens: mockTokens,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        });
      },

      logout: () => {
        set({
          user: null,
          tokens: null,
          isAuthenticated: false,
          isLoading: false,
          error: null,
        });
      },

      setUser: (user: User) => set({ user }),
      setLoading: (isLoading: boolean) => set({ isLoading }),
      clearError: () => set({ error: null }),
    }),
    {
      name: 'ledgerai-auth',
      partialize: (state) => ({
        user: state.user,
        tokens: state.tokens,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
