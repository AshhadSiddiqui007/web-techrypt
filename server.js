const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// MongoDB connection
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log('✅ MongoDB connected'))
.catch((err) => console.error('❌ MongoDB connection error:', err));

// Sample route
app.get('/', (req, res) => {
  res.send('Hello from backend');
});

// Start server
const PORT = process.env.NODE_PORT || 3000;  // Changed to port 3000 to avoid conflict with Python Flask (port 5000)
app.listen(PORT, () => {
  console.log(`🚀 Node.js Server running on port ${PORT}`);
  console.log(`📡 Access at: http://localhost:${PORT}`);
  console.log(`ℹ️  Python Flask backend should be running on port 5000 for appointments`);
});
