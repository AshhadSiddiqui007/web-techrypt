import React, { useState, useEffect } from 'react';
import { FiCalendar, FiClock, FiUser, FiMail, FiPhone, FiEdit, FiTrash2, FiEye } from 'react-icons/fi';

const AppointmentManagement = () => {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedAppointment, setSelectedAppointment] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [statusFilter, setStatusFilter] = useState('all');

  const API_BASE_URL = import.meta.env.VITE_NODE_BACKEND;

  // Get auth token from localStorage
  const getAuthToken = () => {
    return localStorage.getItem('adminToken');
  };

  // Fetch all appointments
  const fetchAppointments = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/appointments`);
      const data = await response.json();
      if (data.success) {
        setAppointments(data.appointments);
      }
    } catch (error) {
      console.error('Error fetching appointments:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAppointments();
  }, []);

  // Update appointment status
  const updateAppointmentStatus = async (appointmentId, newStatus) => {
    const token = getAuthToken();
    if (!token) {
      alert('You must be logged in to perform this action');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/appointments/${appointmentId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ status: newStatus })
      });

      const data = await response.json();
      
      if (data.success) {
        fetchAppointments(); // Refresh the list
        alert('Appointment status updated successfully!');
      } else {
        alert('Error updating appointment status');
      }
    } catch (error) {
      console.error('Error updating appointment:', error);
      alert('Error updating appointment');
    }
  };

  // Format date
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  // Filter appointments by status
  const filteredAppointments = appointments.filter(appointment => {
    if (statusFilter === 'all') return true;
    return appointment.status.toLowerCase() === statusFilter.toLowerCase();
  });

  // Get status color
  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'pending':
        return 'bg-yellow-600 text-yellow-100';
      case 'confirmed':
        return 'bg-green-600 text-green-100';
      case 'cancelled':
        return 'bg-red-600 text-red-100';
      case 'completed':
        return 'bg-blue-600 text-blue-100';
      default:
        return 'bg-gray-600 text-gray-100';
    }
  };

  // View appointment details
  const viewAppointmentDetails = (appointment) => {
    setSelectedAppointment(appointment);
    setShowModal(true);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-white text-xl">Loading appointments...</div>
      </div>
    );
  }

  return (
    <div className="text-white">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold">Appointment Management</h2>
        <div className="flex items-center gap-4">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 bg-[#1a1a1a] border border-gray-700 rounded-lg text-white"
          >
            <option value="all">All Appointments</option>
            <option value="pending">Pending</option>
            <option value="confirmed">Confirmed</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-[#1a1a1a] p-4 rounded-lg border border-gray-700">
          <h3 className="text-sm text-gray-400">Total Appointments</h3>
          <p className="text-2xl font-bold text-primary">{appointments.length}</p>
        </div>
        <div className="bg-[#1a1a1a] p-4 rounded-lg border border-gray-700">
          <h3 className="text-sm text-gray-400">Pending</h3>
          <p className="text-2xl font-bold text-yellow-400">
            {appointments.filter(a => a.status.toLowerCase() === 'pending').length}
          </p>
        </div>
        <div className="bg-[#1a1a1a] p-4 rounded-lg border border-gray-700">
          <h3 className="text-sm text-gray-400">Confirmed</h3>
          <p className="text-2xl font-bold text-green-400">
            {appointments.filter(a => a.status.toLowerCase() === 'confirmed').length}
          </p>
        </div>
        <div className="bg-[#1a1a1a] p-4 rounded-lg border border-gray-700">
          <h3 className="text-sm text-gray-400">Completed</h3>
          <p className="text-2xl font-bold text-blue-400">
            {appointments.filter(a => a.status.toLowerCase() === 'completed').length}
          </p>
        </div>
      </div>

      {/* Appointments List */}
      <div className="bg-[#1a1a1a] rounded-lg overflow-hidden border border-gray-700">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-[#1a1a1a]">
              <tr>
                <th className="px-6 py-3 text-left">Client</th>
                <th className="px-6 py-3 text-left">Contact</th>
                <th className="px-6 py-3 text-left">Services</th>
                <th className="px-6 py-3 text-left">Date & Time</th>
                <th className="px-6 py-3 text-left">Status</th>
                <th className="px-6 py-3 text-left">Booked On</th>
                <th className="px-6 py-3 text-left">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800">
              {filteredAppointments.map((appointment) => (
                <tr key={appointment._id} className="hover:bg-[#252525]">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <FiUser className="text-gray-400" />
                      <div>
                        <div className="font-medium">{appointment.name}</div>
                        <div className="text-sm text-gray-400">ID: {appointment._id.slice(-8)}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="space-y-1">
                      <div className="flex items-center gap-1 text-sm">
                        <FiMail className="text-gray-400" />
                        {appointment.email}
                      </div>
                      <div className="flex items-center gap-1 text-sm">
                        <FiPhone className="text-gray-400" />
                        {appointment.phone}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="space-y-1">
                      {appointment.services?.map((service, index) => (
                        <span key={index} className="inline-block bg-gray-700 px-2 py-1 rounded text-xs mr-1">
                          {service}
                        </span>
                      )) || 'No services specified'}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="space-y-1">
                      <div className="flex items-center gap-1 text-sm">
                        <FiCalendar className="text-gray-400" />
                        {appointment.preferred_date}
                      </div>
                      <div className="flex items-center gap-1 text-sm">
                        <FiClock className="text-gray-400" />
                        {appointment.preferred_time}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <select
                      value={appointment.status}
                      onChange={(e) => updateAppointmentStatus(appointment._id, e.target.value)}
                      className={`px-2 py-1 rounded text-xs ${getStatusColor(appointment.status)} border-none`}
                    >
                      <option value="Pending">Pending</option>
                      <option value="Confirmed">Confirmed</option>
                      <option value="Completed">Completed</option>
                      <option value="Cancelled">Cancelled</option>
                    </select>
                  </td>
                  <td className="px-6 py-4">{formatDate(appointment.created_at)}</td>
                  <td className="px-6 py-4">
                    <button
                      onClick={() => viewAppointmentDetails(appointment)}
                      className="text-blue-400 hover:text-blue-300 p-1"
                      title="View Details"
                    >
                      <FiEye />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {filteredAppointments.length === 0 && (
          <div className="text-center py-8 text-gray-400">
            No appointments found for the selected filter.
          </div>
        )}
      </div>

      {/* Modal for appointment details */}
      {showModal && selectedAppointment && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-[#1a1a1a] rounded-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto border border-gray-700">
            <div className="p-6">
              {/* Modal Header */}
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-2xl font-bold">Appointment Details</h3>
                <button
                  onClick={() => setShowModal(false)}
                  className="text-gray-400 hover:text-white"
                >
                  ×
                </button>
              </div>

              {/* Appointment Details */}
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1 text-gray-400">Client Name</label>
                    <p className="text-white">{selectedAppointment.name}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1 text-gray-400">Status</label>
                    <span className={`px-2 py-1 rounded text-xs ${getStatusColor(selectedAppointment.status)}`}>
                      {selectedAppointment.status}
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1 text-gray-400">Email</label>
                    <p className="text-white">{selectedAppointment.email}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1 text-gray-400">Phone</label>
                    <p className="text-white">{selectedAppointment.phone}</p>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1 text-gray-400">Preferred Date</label>
                    <p className="text-white">{selectedAppointment.preferred_date}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1 text-gray-400">Preferred Time</label>
                    <p className="text-white">{selectedAppointment.preferred_time}</p>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1 text-gray-400">Services Requested</label>
                  <div className="space-y-1">
                    {selectedAppointment.services?.map((service, index) => (
                      <span key={index} className="inline-block bg-gray-700 px-2 py-1 rounded text-sm mr-2">
                        {service}
                      </span>
                    )) || <p className="text-gray-400">No services specified</p>}
                  </div>
                </div>

                {selectedAppointment.notes && (
                  <div>
                    <label className="block text-sm font-medium mb-1 text-gray-400">Notes</label>
                    <p className="text-white bg-gray-800 p-3 rounded">{selectedAppointment.notes}</p>
                  </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1 text-gray-400">Booked On</label>
                    <p className="text-white">{formatDate(selectedAppointment.created_at)}</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1 text-gray-400">Source</label>
                    <p className="text-white">{selectedAppointment.source || 'Website'}</p>
                  </div>
                </div>
              </div>

              {/* Modal Actions */}
              <div className="flex gap-4 justify-end mt-6">
                <button
                  onClick={() => setShowModal(false)}
                  className="px-6 py-2 bg-gray-600 hover:bg-gray-700 rounded-lg transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AppointmentManagement;