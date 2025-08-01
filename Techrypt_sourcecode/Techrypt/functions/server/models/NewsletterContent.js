const mongoose = require('mongoose');

const newsletterContentSchema = new mongoose.Schema({
  subject: String,
  content: String,
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('NewsletterContent', newsletterContentSchema);