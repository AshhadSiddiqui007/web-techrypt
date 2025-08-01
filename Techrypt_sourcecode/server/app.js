// --- Secure, production-ready Express app.js ---
const express = require('express');
const path = require('path');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const axios = require('axios');
const cron = require('node-cron');

// Load environment variables based on NODE_ENV
const envFile = process.env.NODE_ENV === 'production' ? '../.env.production' : '../.env';
require('dotenv').config({ path: envFile });

// MongoDB connect logic separated
const connectDb = require('./config/database');
connectDb();

// Import routes
const AdminRoutes = require('./routes/AdminRoutes');
const newsletterRoutes = require('./routes/newsletterRoutes');
const appointmentRoutes = require('./routes/appointmentRoutes');
const contactRoutes = require('./routes/contactRoutes');
const blogRoutes = require('./routes/blogRoutes');
const { errorHandlerMiddleWare, notFound } = require('./middlewares/errorHandler');
const NewsletterContent = require('./models/NewsletterContent');
const startScheduledBlogPublisher = require('./utils/schedule');

const app = express();
const PORT = process.env.PORT || 5000;

// CORS configuration
const corsOptions = {
  origin:
    process.env.NODE_ENV === 'production'
      ? process.env.ALLOWED_ORIGINS?.split(',') || ['https://your-domain.com']
      : ['http://localhost:3000', 'http://localhost:5173'],
  credentials: true,
  optionsSuccessStatus: 200,
};
app.use(cors(corsOptions));

// Security headers
app.use(helmet({
  crossOriginResourcePolicy: false,
}));

// Trust proxy
if (process.env.NODE_ENV === 'production') {
  app.set('trust proxy', 1);
}

// Rate limiting
if (process.env.NODE_ENV === 'production') {
  const limiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100,
  });
  app.use('/api/', limiter);
}

// Body parsers
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static images
app.use('/images', express.static(path.join(__dirname, '../Techrypt/public/images')));

// Helpful debug logs
if (process.env.NODE_ENV !== 'production') {
  console.log('=== ENVIRONMENT VARIABLES DEBUG ===');
  console.log('NODE_ENV:', process.env.NODE_ENV);
  console.log('PORT:', process.env.PORT);
  console.log('JWT_SECRET:', process.env.JWT_SECRET ? 'SET' : 'UNDEFINED');
  console.log('MONGODB_URI:', process.env.MONGODB_URI ? 'SET' : 'UNDEFINED');
  console.log('SENDER_EMAIL:', process.env.SENDER_EMAIL ? 'SET' : 'UNDEFINED');
  console.log('SMTP_SERVER:', process.env.SMTP_SERVER);
  console.log('SMTP_PORT:', process.env.SMTP_PORT);
  console.log('=====================================');
}

// --- Request logging middleware (before all routes) ---
app.use((req, res, next) => {
  console.log('Incoming Request:', req.method, req.originalUrl);
  next();
});

// --- API ROUTES ---
app.get('/', (req, res) => {
  res.send('Welcome to Techrypt');
});

// ✅ Test health route for debugging
app.get('/api/test-health', (req, res) => {
  res.json({ status: 'Server is working ✅', time: new Date().toISOString() });
});

app.get('/api/test', (req, res) => {
  res.json({ message: 'API is working', timestamp: new Date().toISOString() });
});

app.use('/admin', AdminRoutes);
app.use('/newsletter', newsletterRoutes);
app.use('/appointments', appointmentRoutes);
app.use('/contact', contactRoutes);
// Mount blogRoutes at '/blogs' to match NGINX config (which strips '/api/')
app.use('/blogs', blogRoutes);

// Dev logs for reference
if (process.env.NODE_ENV !== 'production') {
  console.log('Newsletter routes mounted at /api/newsletter');
  console.log('Available endpoints:');
  console.log('POST /api/newsletter/subscribe');
  console.log('POST /api/contact-info');
  console.log('POST /api/newsletter/save-newsletter');
  console.log('POST /api/newsletter/send-newsletter');
  console.log('GET /api/newsletter/latest-newsletter');
}

// Cron job for sending newsletter
cron.schedule('0 9 1 * *', async () => {
  try {
    const latest = await NewsletterContent.findOne().sort({ createdAt: -1 });
    if (!latest) return;
    await axios.post(`${process.env.BACKEND_URL || 'http://localhost:5000'}/api/newsletter/send-newsletter`, {
      subject: latest.subject,
      content: latest.content,
    });
    if (process.env.NODE_ENV !== 'production') {
      console.log('Monthly newsletter sent:', latest.subject);
    }
  } catch (err) {
    console.error('Error sending monthly newsletter:', err);
  }
});
startScheduledBlogPublisher();

// Error handling
app.use(notFound);
app.use(errorHandlerMiddleWare);

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
