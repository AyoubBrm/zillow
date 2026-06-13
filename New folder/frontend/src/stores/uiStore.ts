import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface UiStore {
  sidebarCollapsed: boolean;
  sidebarMobileOpen: boolean;
  theme: 'dark' | 'light';
  activeOrgId: string;
  commandPaletteOpen: boolean;
  toggleSidebar: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
  toggleMobileSidebar: () => void;
  closeMobileSidebar: () => void;
  setTheme: (theme: 'dark' | 'light') => void;
  setActiveOrg: (orgId: string) => void;
  toggleCommandPalette: () => void;
}

export const useUiStore = create<UiStore>()(
  persist(
    (set) => ({
      sidebarCollapsed: false,
      sidebarMobileOpen: false,
      theme: 'dark',
      activeOrgId: 'org_5e6f7g8h',
      commandPaletteOpen: false,

      toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
      setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),
      toggleMobileSidebar: () => set((state) => ({ sidebarMobileOpen: !state.sidebarMobileOpen })),
      closeMobileSidebar: () => set({ sidebarMobileOpen: false }),
      setTheme: (theme) => set({ theme }),
      setActiveOrg: (orgId) => set({ activeOrgId: orgId }),
      toggleCommandPalette: () => set((state) => ({ commandPaletteOpen: !state.commandPaletteOpen })),
    }),
    {
      name: 'ledgerai-ui',
      partialize: (state) => ({
        sidebarCollapsed: state.sidebarCollapsed,
        theme: state.theme,
        activeOrgId: state.activeOrgId,
      }),
    }
  )
);
