const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');

// Use the model from the main connection
const NewsletterSubscriber = mongoose.model('NewsletterSubscriber');

router.post('/subscribe-newsletter', async (req, res) => {
  console.log('Newsletter subscription endpoint hit');
  try {
    const { email } = req.body;
    if (!email || !email.includes('@')) {
      return res.status(400).json({ success: false, error: 'Invalid email address' });
    }
    const subscriber = new NewsletterSubscriber({ email: email.trim().toLowerCase() });
    await subscriber.save();
    res.json({ success: true, message: 'Successfully subscribed to newsletter' });
  } catch (err) {
    if (err.code === 11000) {
      res.status(400).json({ success: false, error: 'Email already subscribed' });
    } else {
      res.status(500).json({ success: false, error: err.message });
    }
  }
});

module.exports = router;