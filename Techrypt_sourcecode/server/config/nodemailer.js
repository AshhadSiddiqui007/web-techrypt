const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
    // your SMTP config here
});

module.exports = transporter;