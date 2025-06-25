import React from 'react';
import { MdArticle, MdCalendarToday, MdPerson, MdTrendingUp } from 'react-icons/md';

const StatCard = ({ title, value, icon, color }) => (
  <div className="bg-[#1a1a1a] rounded-lg p-6 shadow-lg">
    <div className="flex justify-between items-center">
      <div>
        <p className="text-gray-400 text-sm">{title}</p>
        <h3 className="text-2xl font-bold text-white mt-2">{value}</h3>
      </div>
      <div className={`p-3 rounded-full ${color}`}>
        {icon}
      </div>
    </div>
  </div>
);

const AdminDashboardHome = () => {
  // In a real application, you would fetch this data from your backend
  const stats = [
    { title: 'Total Blogs', value: '24', icon: <MdArticle size={24} />, color: 'bg-blue-500/20 text-blue-500' },
    { title: 'Appointments', value: '12', icon: <MdCalendarToday size={24} />, color: 'bg-green-500/20 text-green-500' },
    { title: 'Users', value: '156', icon: <MdPerson size={24} />, color: 'bg-purple-500/20 text-purple-500' },
    { title: 'Page Views', value: '2,345', icon: <MdTrendingUp size={24} />, color: 'bg-primary/20 text-primary' },
  ];

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6 text-white">Dashboard Overview</h2>
      
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, index) => (
          <StatCard key={index} {...stat} />
        ))}
      </div>

      {/* Recent Activity */}
      <div className="bg-[#1a1a1a] rounded-lg p-6 mb-8">
        <h3 className="text-xl font-bold text-white mb-4">Recent Activity</h3>
        <div className="space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="flex items-center py-3 border-b border-gray-800">
              <div className="bg-primary/20 p-2 rounded-full mr-4">
                <MdArticle className="text-primary" size={20} />
              </div>
              <div>
                <p className="text-white font-medium">New blog post published</p>
                <p className="text-gray-400 text-sm">June {20 + i}, 2025</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboardHome;