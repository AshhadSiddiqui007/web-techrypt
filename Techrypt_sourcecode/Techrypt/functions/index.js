const functions = require('firebase-functions');
const admin = require('firebase-admin');
const express = require('express');
const cors = require('cors');
const path = require('path');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

// Import routes
const AdminRoutes = require('../server/routes/AdminRoutes');
const newsletterRoutes = require('../server/routes/newsletterRoutes');
const appointmentRoutes = require('../server/routes/appointmentRoutes');
const contactRoutes = require('../server/routes/contactRoutes');
const blogRoutes = require('../server/routes/blogRoutes');
const { errorHandlerMiddleWare, notFound } = require('../server/middlewares/errorHandler');
const connectDb = require('../server/config/database');

// Initialize Firebase Admin
admin.initializeApp();

// Initialize express app
const app = express();

// Connect to database
connectDb();

// CORS configuration
const corsOptions = {
  origin: ['https://techrypt-uitest.web.app', 'http://localhost:5173'],
  credentials: true,
  optionsSuccessStatus: 200,
};
app.use(cors(corsOptions));

// Security headers
app.use(helmet({
  crossOriginResourcePolicy: false,
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
});
app.use('/api/', limiter);

// Body parsers
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// --- API ROUTES ---
app.get('/', (req, res) => {
  res.send('Welcome to Techrypt API');
});

// Health check route
app.get('/api/test-health', (req, res) => {
  res.json({ status: 'Server is working ✅', time: new Date().toISOString() });
});

app.use('/admin', AdminRoutes);
app.use('/newsletter', newsletterRoutes);
app.use('/appointments', appointmentRoutes);
app.use('/contact', contactRoutes);
app.use('/blogs', blogRoutes);

// Error handling
app.use(notFound);
app.use(errorHandlerMiddleWare);

// Export the API as a Firebase Function
exports.api = functions.https.onRequest(app);
