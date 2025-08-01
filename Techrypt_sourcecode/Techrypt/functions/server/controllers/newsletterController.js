const NewsletterSubscriber = require('../models/Newsletter');
const NewsletterContent = require('../models/NewsletterContent');
const nodemailer = require('nodemailer');

exports.subscribe = async (req, res) => {
    try {
        const { email } = req.body;
        console.log('Newsletter subscription request:', email);
        
        if (!email || !email.includes('@')) {
            console.log('Invalid email:', email);
            return res.status(400).json({ success: false, error: 'Invalid email address' });
        }
        
        const subscriber = new NewsletterSubscriber({ email: email.trim().toLowerCase() });
        await subscriber.save();
        console.log('Successfully subscribed:', email);
        res.json({ success: true, message: 'Successfully subscribed to newsletter' });
    } catch (err) {
        console.error('Newsletter subscription error:', err);
        if (err.code === 11000) {
            res.status(400).json({ success: false, error: 'Email already subscribed' });
        } else {
            res.status(500).json({ success: false, error: err.message });
        }
    }
};

exports.sendNewsletter = async (req, res) => {
    try {
        const { subject, content } = req.body;
        const subscribers = await NewsletterSubscriber.find({});
        const emails = subscribers.map(sub => sub.email);

        const transporter = nodemailer.createTransport({
            host: 'smtp.hostinger.com',
            port: 465,
            secure: true,
            auth: {
                user: process.env.EMAIL_USER,
                pass: process.env.EMAIL_PASS,
            },
        });

        await transporter.sendMail({
            from: process.env.EMAIL_USER,
            to: emails,
            subject,
            html: content,
        });

        res.json({ success: true, message: 'Newsletter sent to all subscribers.' });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
};

exports.saveNewsletterContent = async (req, res) => {
    try {
        const { subject, content } = req.body;
        const newsletter = new NewsletterContent({ subject, content });
        await newsletter.save();
        res.json({ success: true, message: 'Newsletter saved for next send.' });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
};

exports.getLatestNewsletter = async (req, res) => {
    try {
        const latest = await NewsletterContent.findOne().sort({ createdAt: -1 });
        if (!latest) return res.status(404).json({ message: 'No newsletter found' });
        res.json(latest);
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
};

exports.getNewsletterStats = async (req, res) => {
    try {
        // Replace this with your real visitor tracking logic if you have it
        const visitorCount = 0; // Placeholder, update if you track visitors

        const newsletterCount = await NewsletterSubscriber.countDocuments();

        res.json({
            visitorCount,
            newsletterCount,
        });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
};