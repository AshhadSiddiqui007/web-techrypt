const express = require('express');
const router = express.Router();
const contactController = require('../controllers/contactController');

// Submit contact info
router.post('/contact-info', contactController.submit);

// Get all contact info
router.get('/contact-info', contactController.getAll);

module.exports = router;