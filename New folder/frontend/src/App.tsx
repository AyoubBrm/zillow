import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

import AuthLayout from './components/layout/AuthLayout';
import DashboardLayout from './components/layout/DashboardLayout';
import LoginPage from './pages/auth/LoginPage';
import DashboardPage from './pages/dashboard/DashboardPage';

// Placeholder pages to avoid errors
const PlaceholderPage = ({ title }: { title: string }) => (
  <div className="p-8"><h1 className="text-2xl font-bold text-white mb-4">{title}</h1><p className="text-slate-400">Coming soon in Phase 2.</p></div>
);

// Protected Route wrapper
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  // Hardcoded for MVP display until auth is fully hooked up
  const isAuthenticated = true;
  if (!isAuthenticated) return <Navigate to="/login" />;
  return <DashboardLayout>{children}</DashboardLayout>;
};

function App() {
  return (
    <BrowserRouter>
      <Toaster position="top-right" toastOptions={{ className: 'glass-card text-white' }} />
      <Routes>
        {/* Auth Routes */}
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<PlaceholderPage title="Register" />} />
        </Route>

        {/* Protected Dashboard Routes */}
        <Route element={<ProtectedRoute><></></ProtectedRoute>}>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/transactions" element={<PlaceholderPage title="Transactions" />} />
          <Route path="/invoices" element={<PlaceholderPage title="Invoices" />} />
          <Route path="/receipts" element={<PlaceholderPage title="Receipts" />} />
          <Route path="/reports" element={<PlaceholderPage title="Reports" />} />
          <Route path="/settings" element={<PlaceholderPage title="Settings" />} />
        </Route>
        
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
