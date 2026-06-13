import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  ArrowLeftRight,
  FileText,
  Receipt,
  BarChart3,
  Settings,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  LogOut,
  CreditCard,
} from 'lucide-react';
import { useUiStore } from '../../stores/uiStore';
import { useAuthStore } from '../../stores/authStore';
import Avatar from '../ui/Avatar';

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/transactions', label: 'Transactions', icon: ArrowLeftRight },
  { path: '/invoices', label: 'Invoices', icon: FileText },
  { path: '/receipts', label: 'Receipts', icon: Receipt },
  { path: '/reports', label: 'Reports', icon: BarChart3 },
  { path: '/settings', label: 'Settings', icon: Settings },
];

const Sidebar: React.FC = () => {
  const { sidebarCollapsed, toggleSidebar, sidebarMobileOpen, closeMobileSidebar } = useUiStore();
  const { user, logout } = useAuthStore();
  const location = useLocation();

  return (
    <>
      {/* Mobile Overlay */}
      {sidebarMobileOpen && (
        <div
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
          onClick={closeMobileSidebar}
        />
      )}

      <aside
        id="sidebar"
        className={`
          fixed top-0 left-0 z-50 h-screen
          bg-[#0c1222]/95 backdrop-blur-xl
          border-r border-white/5
          flex flex-col
          transition-all duration-300 ease-out
          ${sidebarCollapsed ? 'w-[72px]' : 'w-[260px]'}
          ${sidebarMobileOpen ? 'translate-x-0' : '-translate-x-full'}
          lg:translate-x-0
        `}
      >
        {/* Logo */}
        <div className={`flex items-center gap-3 px-4 h-16 border-b border-white/5 flex-shrink-0 ${sidebarCollapsed ? 'justify-center' : ''}`}>
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center flex-shrink-0 shadow-lg shadow-violet-500/25">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          {!sidebarCollapsed && (
            <div className="animate-fadeIn">
              <h1 className="text-lg font-bold text-white tracking-tight">
                Ledger<span className="text-violet-400">AI</span>
              </h1>
            </div>
          )}
        </div>

        {/* Navigation */}
        <nav className="flex-1 py-4 px-2 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const isActive =
              item.path === '/'
                ? location.pathname === '/'
                : location.pathname.startsWith(item.path);

            return (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={closeMobileSidebar}
                id={`nav-${item.label.toLowerCase()}`}
                className={`
                  flex items-center gap-3 px-3 py-2.5 rounded-xl
                  transition-all duration-200 group relative
                  ${sidebarCollapsed ? 'justify-center' : ''}
                  ${
                    isActive
                      ? 'bg-gradient-to-r from-violet-500/15 to-indigo-500/10 text-white'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
                  }
                `}
              >
                {isActive && (
                  <div className="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-6 rounded-r-full bg-gradient-to-b from-violet-400 to-indigo-500" />
                )}
                <item.icon
                  className={`w-5 h-5 flex-shrink-0 transition-colors ${
                    isActive ? 'text-violet-400' : 'text-slate-500 group-hover:text-slate-300'
                  }`}
                />
                {!sidebarCollapsed && (
                  <span className="text-sm font-medium animate-fadeIn">{item.label}</span>
                )}
                {sidebarCollapsed && (
                  <div className="absolute left-full ml-2 px-2.5 py-1.5 bg-slate-800 text-slate-200 text-xs font-medium rounded-lg whitespace-nowrap opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50 shadow-xl border border-slate-700/50">
                    {item.label}
                  </div>
                )}
              </NavLink>
            );
          })}
        </nav>

        {/* Quick Stats */}
        {!sidebarCollapsed && (
          <div className="mx-3 mb-3 p-3 rounded-xl bg-gradient-to-br from-violet-500/10 to-indigo-500/5 border border-violet-500/10 animate-fadeIn">
            <div className="flex items-center gap-2 mb-2">
              <CreditCard className="w-4 h-4 text-violet-400" />
              <span className="text-xs font-medium text-slate-300">Pro Plan</span>
            </div>
            <div className="text-xs text-slate-500">
              156 of 500 transactions used
            </div>
            <div className="mt-2 h-1.5 bg-slate-700/50 rounded-full overflow-hidden">
              <div className="h-full w-[31%] bg-gradient-to-r from-violet-500 to-indigo-500 rounded-full" />
            </div>
          </div>
        )}

        {/* User Section */}
        <div className={`border-t border-white/5 p-3 flex-shrink-0 ${sidebarCollapsed ? 'flex justify-center' : ''}`}>
          {sidebarCollapsed ? (
            <Avatar name={user ? `${user.firstName} ${user.lastName}` : 'User'} size="sm" />
          ) : (
            <div className="flex items-center gap-3 animate-fadeIn">
              <Avatar name={user ? `${user.firstName} ${user.lastName}` : 'User'} size="sm" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-slate-200 truncate">
                  {user ? `${user.firstName} ${user.lastName}` : 'User'}
                </p>
                <p className="text-xs text-slate-500 truncate">{user?.email || 'user@email.com'}</p>
              </div>
              <button
                onClick={logout}
                className="p-1.5 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
                id="sidebar-logout-btn"
                title="Sign out"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>

        {/* Collapse Toggle */}
        <button
          onClick={toggleSidebar}
          className="hidden lg:flex absolute -right-3 top-20 w-6 h-6 bg-slate-800 border border-slate-700/50 rounded-full items-center justify-center text-slate-400 hover:text-white hover:bg-slate-700 transition-all z-50 shadow-lg"
          id="sidebar-collapse-btn"
        >
          {sidebarCollapsed ? (
            <ChevronRight className="w-3.5 h-3.5" />
          ) : (
            <ChevronLeft className="w-3.5 h-3.5" />
          )}
        </button>
      </aside>
    </>
  );
};

export default Sidebar;
