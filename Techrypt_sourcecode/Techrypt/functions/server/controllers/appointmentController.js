const Appointment = require('../models/Appointment');

exports.book = async (req, res) => {
    try {
        const appointment = new Appointment(req.body);
        await appointment.save();
        res.json({ success: true, message: 'Appointment booked successfully', appointment });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
};

exports.getAll = async (req, res) => {
    try {
        const appointments = await Appointment.find();
        res.json({ success: true, appointments });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
};

exports.update = async (req, res) => {
    try {
        const appointment = await Appointment.findByIdAndUpdate(
            req.params.id,
            req.body,
            { new: true }
        );
        if (!appointment) {
            return res.status(404).json({ success: false, error: 'Appointment not found' });
        }
        res.json({ success: true, appointment });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
};