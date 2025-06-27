import React from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import AdminSidebar from '../../components/AdminDashboard/AdminSidebar.jsx';
import AdminDashboardHome from '../../components/AdminDashboard/AdminDashboardHome.jsx';
import BlogManagement from '../../components/AdminDashboard/BlogManagement.jsx';
import AppointmentManagement from '../../components/AdminDashboard/AppointmentManagement.jsx';
import ProtectedRoute from '../../components/AdminDashboard/ProtectedRoute.jsx';

const AdminDashboard = () => {
  const location = useLocation();
  const currentPath = location.pathname.split('/').pop() || 'dashboard';

  return (
    <ProtectedRoute>
      <div className="flex h-screen bg-[#0f0f0f] fixed inset-0">
        {/* Sidebar */}
        <AdminSidebar currentSection={currentPath} />
        
        {/* Main Content Area - Scrollable */}
        <div className="flex-1 overflow-y-auto">
          <div className="p-6">
            <Routes>
              <Route path="/" element={<AdminDashboardHome />} />
              <Route path="dashboard" element={<AdminDashboardHome />} />
              <Route path="blogs" element={<BlogManagement />} />
              <Route path="appointments" element={<AppointmentManagement />} />
              <Route path="*" element={<Navigate to="dashboard" replace />} />
            </Routes>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default AdminDashboard;