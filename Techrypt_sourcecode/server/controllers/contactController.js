const Contact = require('../models/Contact');

exports.submit = async (req, res) => {
    try {
        const contact = new Contact(req.body);
        await contact.save();
        res.json({ success: true, message: 'Contact info submitted successfully', contact });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
};

exports.getAll = async (req, res) => {
    try {
        const contacts = await Contact.find();
        res.json({ success: true, contacts });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
}; 