import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';
import { useUiStore } from '../../stores/uiStore';
import ChatWidget from '../ai/ChatWidget';

const DashboardLayout: React.FC = () => {
  const { sidebarCollapsed } = useUiStore();

  return (
    <div className="min-h-screen bg-[#0a0e1a]">
      <Sidebar />

      <div
        className={`transition-all duration-300 ${
          sidebarCollapsed ? 'lg:ml-[72px]' : 'lg:ml-[260px]'
        }`}
      >
        <Header />

        <main className="p-4 lg:p-6 min-h-[calc(100vh-64px)]">
          <div className="animate-fadeIn">
            <Outlet />
          </div>
        </main>
      </div>

      <ChatWidget />
    </div>
  );
};

export default DashboardLayout;
