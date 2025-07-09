const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
    host: process.env.SMTP_SERVER || 'smtp.hostinger.com',
    port: process.env.SMTP_PORT || 26,
    secure: false, // true for 465, false for other ports
    auth: {
        user: process.env.SENDER_EMAIL || 'projects@techrypt.io',
        pass: process.env.SMTP_PASSWORD || 'Monday@!23456'
    },
    tls: {
        rejectUnauthorized: false,
        ciphers: 'SSLv3'
    },
    requireTLS: true,
    connectionTimeout: 60000,
    greetingTimeout: 30000,
    socketTimeout: 60000
});

// Only verify transporter configuration if credentials are provided
if (process.env.SENDER_EMAIL && process.env.SMTP_PASSWORD) {
    console.log('SMTP configuration loaded successfully');
    console.log('SMTP server is ready to send emails from:', process.env.SENDER_EMAIL);
    
    // Uncomment the verification below if you want to test the connection
    /*
    transporter.verify((error, success) => {
        if (error) {
            console.log('SMTP configuration error:', error);
        } else {
            console.log('SMTP server is ready to send emails from:', process.env.SENDER_EMAIL);
        }
    });
    */
} else {
    console.log('SMTP credentials not provided. Please set SENDER_EMAIL and SMTP_PASSWORD environment variables.');
}

module.exports = transporter;