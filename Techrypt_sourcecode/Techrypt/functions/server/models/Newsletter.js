const mongoose = require('mongoose');

const newsletterSchema = new mongoose.Schema({
    email: { type: String, unique: true },
    subscribed_at: { type: Date, default: Date.now }
}, { collection: 'newslettersubscribers' });

module.exports = mongoose.model('NewsletterSubscriber', newsletterSchema);