const express = require('express');
const router = express.Router();
const appointmentController = require('../controllers/appointmentController');

// Book a new appointment
router.post('/appointments', appointmentController.book);

// Get all appointments
router.get('/appointments', appointmentController.getAll);

// Update an appointment by ID
router.put('/appointments/:id', appointmentController.update);

module.exports = router;