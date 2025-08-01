const mongoose = require('mongoose');

const contactSchema = new mongoose.Schema({
    name: String,
    email: String,
    phone: String,
    submitted_at: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Contact_Info', contactSchema);