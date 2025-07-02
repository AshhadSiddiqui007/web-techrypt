const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
    service: 'gmail', // You can change this to your preferred email service
    auth: {
        user: process.env.SMTP_USER || 'your-email@gmail.com', // Add to .env file
        pass: process.env.SMTP_PASS || 'your-app-password'     // Add to .env file
    },
    tls: {
        rejectUnauthorized: false
    }
});

// Verify transporter configuration
transporter.verify((error, success) => {
    if (error) {
        console.log('SMTP configuration error:', error);
    } else {
        console.log('SMTP server is ready to send emails');
    }
});

module.exports = transporter;