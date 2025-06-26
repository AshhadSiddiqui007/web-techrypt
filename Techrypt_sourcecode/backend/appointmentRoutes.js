const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');

// --- Appointment Schema (reuse or import if already defined) ---
const appointmentSchema = new mongoose.Schema({
  name: String,
  email: String,
  phone: String,
  business_type: String,
  services: [String],
  preferred_date: String,
  preferred_time: String,
  notes: String,
  status: { type: String, default: 'Pending' },
  source: { type: String, default: 'api' },
  created_at: { type: Date, default: Date.now }
});
const Appointment = mongoose.models.Appointment || mongoose.model('Appointment Data', appointmentSchema);

// --- POST /api/appointments ---
router.post('/appointments', async (req, res) => {
  try {
    const data = req.body;
    if (!data) {
      return res.status(400).json({ error: 'No data provided' });
    }

    // Extract and normalize appointment data
    const appointmentData = {
      name: (data.name || '').trim(),
      email: (data.email || '').trim(),
      phone: (data.phone || '').trim(),
      business_type: (data.business_type || '').trim(),
      services: data.services || data.services_interested || [],
      preferred_date: (data.preferred_date || '').trim(),
      preferred_time: (data.preferred_time || '').trim(),
      notes: (data.notes || data.message || '').trim(),
      status: data.status || 'Pending',
      source: data.source || 'api',
      created_at: data.created_at ? new Date(data.created_at) : new Date()
    };

    // Validate required fields
    if (!appointmentData.name || !appointmentData.email) {
      return res.status(400).json({ error: 'Name and email are required' });
    }

    // Save to MongoDB
    const appointment = new Appointment(appointmentData);
    await appointment.save();

    // Confirmation message
    const servicesText = Array.isArray(appointmentData.services) && appointmentData.services.length
      ? appointmentData.services.join(', ')
      : 'To be discussed';

    const confirmationMessage = `✅ Appointment Booked Successfully!

📅 Appointment Details:
• Name: ${appointmentData.name}
• Email: ${appointmentData.email}
• Services: ${servicesText}
• Preferred Date: ${appointmentData.preferred_date || 'Flexible'}
• Preferred Time: ${appointmentData.preferred_time || 'Flexible'}

🎯 Next Steps:
1. You'll receive a confirmation email within 24 hours
2. Our team will contact you to confirm the appointment time
3. We'll prepare a customized consultation based on your business needs

Thank you for choosing Techrypt! We're excited to help grow your business.`;

    return res.json({
      success: true,
      message: confirmationMessage,
      appointment_id: appointment._id,
      status: 'confirmed',
      timestamp: appointmentData.created_at,
      saved_to_database: true
    });

  } catch (e) {
    console.error('❌ Appointment booking error:', e);
    return res.status(500).json({
      error: 'Failed to book appointment. Please try again.',
      success: false
    });
  }
});

module.exports = router;