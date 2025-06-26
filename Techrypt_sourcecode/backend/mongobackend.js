const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const nodemailer = require('nodemailer');

const app = express();
app.use(express.json());
app.use(cors());

// --- MongoDB Connection ---
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/TechryptAppoinment';
mongoose.connect(MONGODB_URI);

// --- Schemas ---
const userSchema = new mongoose.Schema({
  name: String,
  email: { type: String, unique: true },
  phone: String,
  business_type: String,
  created_at: { type: Date, default: Date.now },
  last_interaction: { type: Date, default: Date.now },
  metadata: Object
});

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
}, { collection: 'Appointment data' }); // <-- exact collection name

const conversationSchema = new mongoose.Schema({
  id: String,
  user_name: String,
  user_message: String,
  bot_response: String,
  business_type: String,
  model: String,
  response_time: String,
  timestamp: { type: Date, default: Date.now },
  metadata: Object
});

const contactInfoSchema = new mongoose.Schema({
  name: String,
  email: String,
  phone: String,
  submitted_at: { type: Date, default: Date.now }
});

const newsletterSchema = new mongoose.Schema({
  email: { type: String, unique: true },
  subscribed_at: { type: Date, default: Date.now }
}, { collection: 'newslettersubscribers' });

// --- Models ---
const User = mongoose.model('User', userSchema);
const Appointment = mongoose.model('Appointment', appointmentSchema);
const Conversation = mongoose.model('Conversation', conversationSchema);
const ContactInfo = mongoose.model('ContactInfo', contactInfoSchema);
const NewsletterSubscriber = mongoose.model('NewsletterSubscriber', newsletterSchema);

// --- Email Setup (nodemailer) ---
const transporter = nodemailer.createTransport({
  host: process.env.SMTP_SERVER || 'smtp.hostinger.com',
  port: process.env.SMTP_PORT || 587,
  secure: false,
  auth: {
    user: process.env.SENDER_EMAIL || 'projects@techrypt.io',
    pass: process.env.SMTP_PASSWORD || 'Monday@!23456'
  }
});

// --- API Endpoints ---

// User Management
app.post('/api/users', async (req, res) => {
  try {
    const user = new User(req.body);
    await user.save();
    res.json({ success: true, user_id: user._id });
  } catch (err) {
    if (err.code === 11000) {
      res.status(400).json({ success: false, error: 'Email already exists' });
    } else {
      res.status(500).json({ success: false, error: err.message });
    }
  }
});

app.get('/api/users', async (req, res) => {
  try {
    const users = await User.find().limit(100);
    res.json({ success: true, users });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// Conversation Management
app.post('/api/conversations', async (req, res) => {
  try {
    const conversation = new Conversation(req.body);
    await conversation.save();
    res.json({ success: true, conversation_id: conversation._id });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

app.get('/api/conversations', async (req, res) => {
  try {
    const { user_name } = req.query;
    let query = {};
    if (user_name) query.user_name = user_name;
    const conversations = await Conversation.find(query).sort({ timestamp: -1 }).limit(100);
    res.json({ success: true, conversations });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// Statistics
app.get('/api/statistics', async (req, res) => {
  try {
    const total_users = await User.countDocuments();
    const total_appointments = await Appointment.countDocuments();
    const total_conversations = await Conversation.countDocuments();
    const pending_appointments = await Appointment.countDocuments({ status: 'Pending' });
    const completed_appointments = await Appointment.countDocuments({ status: 'Completed' });
    res.json({
      total_users,
      total_appointments,
      total_conversations,
      pending_appointments,
      completed_appointments,
      last_updated: new Date().toISOString()
    });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// --- Modular Routes ---
const appointmentRoutes = require('./appointmentRoutes');
const contactRoute = require('./contactRoute');
const newsletterRoute = require('./newsletterRoute');

app.use('/api', appointmentRoutes);
app.use('/api', contactRoute);
app.use('/api', newsletterRoute);

// --- Logging Middleware ---
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.originalUrl}`);
  next();
});

// --- Start Server ---
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Node.js MongoDB backend running on port ${PORT}`));

const handleSubscribe = async (e) => {
  e.preventDefault();
  setStatus("");
  try {
    const res = await fetch("/api/subscribe-newsletter", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });
    const data = await res.json();
    if (res.ok && data.success) {
      setStatus("success");
      setEmail("");
    } else {
      setStatus("error");
    }
  } catch (err) {
    setStatus("error");
  }
};