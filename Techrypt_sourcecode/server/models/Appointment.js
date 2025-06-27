const mongoose = require('mongoose');

const appointmentSchema = new mongoose.Schema({
    name: String,
    email: String,
    phone: String,
    services: [String],
    preferred_date: String,
    preferred_time: String,
    status: { type: String, default: 'Pending' },
    notes: String,
    source: String,
    created_at: { type: Date, default: Date.now },
    updated_at: { type: Date, default: Date.now },
    metadata: Object,
    timezone_info: Object
}, { collection: 'Appointment data' });

module.exports = mongoose.model('Appointment', appointmentSchema);