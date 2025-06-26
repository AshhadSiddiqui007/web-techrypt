const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');

// --- ContactInfo Schema (reuse or import if already defined) ---
const contactInfoSchema = new mongoose.Schema({
  name: String,
  email: String,
  phone: String,
  submitted_at: { type: Date, default: Date.now }
});
const ContactInfo = mongoose.models.ContactInfo || mongoose.model('ContactInfo', contactInfoSchema);

// --- POST /api/contact-info ---
router.post('/contact-info', async (req, res) => {
  try {
    const data = req.body;
    if (!data || !data.name || !data.email) {
      return res.status(400).json({ success: false, error: 'Name and email are required' });
    }

    const contact = new ContactInfo({
      name: data.name.trim(),
      email: data.email.trim(),
      phone: data.phone ? data.phone.trim() : ''
    });

    const savedContact = await contact.save();

    return res.json({
      success: true,
      message: 'Contact info received.',
      inserted_id: savedContact._id
    });
  } catch (e) {
    console.error('❌ Error saving contact info:', e);
    return res.status(500).json({
      success: false,
      error: 'Failed to save contact info. Please try again.'
    });
  }
});

module.exports = router;