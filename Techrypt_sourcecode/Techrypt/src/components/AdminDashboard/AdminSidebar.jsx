import React from 'react';
import { NavLink } from 'react-router-dom';
import { MdDashboard, MdArticle, MdCalendarToday, MdLogout } from 'react-icons/md';
import { useAuth } from '../../context/AuthContext';
import { toast } from 'react-toastify';

const AdminSidebar = ({ currentSection }) => {
  const { logout, admin } = useAuth();
  const handleLogout = () => {
    logout();
    toast.success('Logged out successfully');
  };

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: <MdDashboard size={24} />, path: '/admin/dashboard' },
    { id: 'blogs', label: 'Blog Management', icon: <MdArticle size={24} />, path: '/admin/blogs' },
    { id: 'appointments', label: 'Appointments', icon: <MdCalendarToday size={24} />, path: '/admin/appointments' }
  ];

  return (
    <div className="w-64 h-full bg-[#1a1a1a] border-r border-gray-800 shadow-lg flex flex-col">
      {/* Logo/Header */}
      <div className="p-6 border-b border-gray-800">
        <h1 className="text-2xl font-bold text-white">Admin Panel</h1>
        <p className="text-primary text-sm">Techrypt Dashboard</p>
        {admin && (
          <div className="mt-3 p-2 bg-[#252525] rounded-lg">
            <p className="text-xs text-gray-400">Logged in as:</p>
            <p className="text-sm text-white truncate">{admin.email}</p>
          </div>
        )}
      </div>

      {/* Navigation Menu */}
      <div className="flex-1 py-6">
        <nav>
          <ul>
            {menuItems.map((item) => (
              <li key={item.id} className="mb-2">
                <NavLink
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center w-full px-6 py-3 text-left transition-colors duration-200 
                    ${isActive 
                      ? 'bg-primary text-white' 
                      : 'text-gray-300 hover:bg-[#252525] hover:text-white'}`}
                >
                  <span className="mr-4">{item.icon}</span>
                  {item.label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      </div>

      {/* Logout Button */}
      <div className="p-6 border-t border-gray-800">
        <button 
          onClick={handleLogout}
          className="flex items-center w-full px-4 py-2 text-gray-300 hover:text-white hover:bg-red-600/20 transition-colors duration-200 rounded-lg"
        >
          <MdLogout size={20} className="mr-2" />
          Logout
        </button>
      </div>
    </div>
  );
};

export default AdminSidebar;