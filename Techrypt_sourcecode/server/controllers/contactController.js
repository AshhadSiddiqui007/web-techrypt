const Contact = require('../models/Contact');
const transporter = require('../config/nodemailer');

exports.submit = async (req, res) => {
    try {
        const { name, email, phone, message } = req.body;
        
        // Save to database (only name, email, phone - not message)
        const contactData = { name, email, phone };
        const contact = new Contact(contactData);
        await contact.save();

        // Send email notification to info@techrypt.io
        const mailOptions = {
            from: process.env.SMTP_USER || 'noreply@techrypt.io',
            to: 'info@techrypt.io',
            subject: `New Contact Form Submission from ${name}`,
            html: `
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #1a1a1a; color: white; padding: 20px; border-radius: 10px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h2 style="color: #c4d322; margin: 0;">New Contact Form Submission</h2>
                    </div>
                    
                    <div style="background: #2a2a2a; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                        <h3 style="color: #c4d322; margin-top: 0;">Contact Details:</h3>
                        <p><strong>Name:</strong> ${name}</p>
                        <p><strong>Email:</strong> ${email}</p>
                        <p><strong>Phone:</strong> ${phone || 'Not provided'}</p>
                    </div>
                    
                    ${message ? `
                    <div style="background: #2a2a2a; padding: 20px; border-radius: 8px;">
                        <h3 style="color: #c4d322; margin-top: 0;">Message:</h3>
                        <p style="line-height: 1.6;">${message}</p>
                    </div>
                    ` : ''}
                    
                    <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #444;">
                        <p style="color: #888; font-size: 14px;">This email was sent from the Techrypt contact form.</p>
                    </div>
                </div>
            `
        };

        await transporter.sendMail(mailOptions);

        res.json({ 
            success: true, 
            message: 'Thank you for your message! We\'ll get back to you soon.',
            contact: contactData 
        });
    } catch (err) {
        console.error('Contact submission error:', err);
        res.status(500).json({ 
            success: false, 
            error: 'Failed to submit contact form. Please try again later.' 
        });
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