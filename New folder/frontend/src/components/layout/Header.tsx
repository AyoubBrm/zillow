import React from 'react';
import { useLocation } from 'react-router-dom';
import {
  Menu,
  Bell,
  Search,
  ChevronRight,
} from 'lucide-react';
import { useUiStore } from '../../stores/uiStore';
import { useAuthStore } from '../../stores/authStore';
import Avatar from '../ui/Avatar';
import Dropdown from '../ui/Dropdown';

const routeTitles: Record<string, string> = {
  '/': 'Dashboard',
  '/transactions': 'Transactions',
  '/invoices': 'Invoices',
  '/receipts': 'Receipts',
  '/reports': 'Reports',
  '/settings': 'Settings',
};

const Header: React.FC = () => {
  const { toggleMobileSidebar } = useUiStore();
  const { user, logout } = useAuthStore();
  const location = useLocation();

  const pageTitle = routeTitles[location.pathname] || 'Dashboard';

  const userDropdownItems = [
    { id: 'profile', label: 'Profile Settings', onClick: () => {} },
    { id: 'billing', label: 'Billing & Plans', onClick: () => {} },
    { id: 'divider-1', label: '', divider: true },
    { id: 'docs', label: 'Documentation', onClick: () => {} },
    { id: 'support', label: 'Support', onClick: () => {} },
    { id: 'divider-2', label: '', divider: true },
    { id: 'logout', label: 'Sign Out', danger: true, onClick: logout },
  ];

  return (
    <header
      id="header"
      className="sticky top-0 z-30 h-16 bg-[#0a0e1a]/80 backdrop-blur-xl border-b border-white/5 flex items-center justify-between px-4 lg:px-6"
    >
      {/* Left side */}
      <div className="flex items-center gap-4">
        {/* Mobile menu button */}
        <button
          onClick={toggleMobileSidebar}
          className="lg:hidden p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-colors"
          id="mobile-menu-btn"
        >
          <Menu className="w-5 h-5" />
        </button>

        {/* Breadcrumb */}
        <nav className="flex items-center gap-2 text-sm" id="breadcrumb">
          <span className="text-slate-500">{user?.organizationName || 'Organization'}</span>
          <ChevronRight className="w-3.5 h-3.5 text-slate-600" />
          <span className="text-slate-200 font-medium">{pageTitle}</span>
        </nav>
      </div>

      {/* Right side */}
      <div className="flex items-center gap-3">
        {/* Search */}
        <div className="hidden md:flex items-center">
          <div className="relative group">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
            <input
              type="text"
              placeholder="Search anything... ⌘K"
              className="w-64 bg-slate-800/40 border border-slate-700/30 rounded-xl pl-10 pr-4 py-2 text-sm text-slate-300 placeholder-slate-500 focus:outline-none focus:border-violet-500/40 focus:ring-1 focus:ring-violet-500/20 focus:w-80 transition-all duration-300"
              id="header-search"
            />
          </div>
        </div>

        {/* Notifications */}
        <button
          className="relative p-2 rounded-xl text-slate-400 hover:text-white hover:bg-white/5 transition-colors"
          id="notification-bell"
        >
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-violet-500 rounded-full ring-2 ring-[#0a0e1a]" />
        </button>

        {/* User dropdown */}
        <Dropdown
          trigger={
            <div className="flex items-center gap-2 p-1.5 rounded-xl hover:bg-white/5 transition-colors cursor-pointer">
              <Avatar name={user ? `${user.firstName} ${user.lastName}` : 'User'} size="sm" />
              <span className="hidden sm:block text-sm text-slate-300 font-medium">
                {user?.firstName || 'User'}
              </span>
            </div>
          }
          items={userDropdownItems}
          id="user-dropdown"
        />
      </div>
    </header>
  );
};

export default Header;
