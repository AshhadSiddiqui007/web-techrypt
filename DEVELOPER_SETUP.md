# 🚀 Techrypt Full-Stack Application - Developer Setup Guide

## Quick Setup for New Developers

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Git

### One-Command Setup
```bash
npm run setup
```

This will install all dependencies for:
- Root project (concurrently, etc.)
- Node.js server (Express, MongoDB, etc.)
- React frontend (Vite, React, etc.)
- Python chatbot (Flask, AI libraries, etc.)

### Manual Setup (if needed)

1. **Install root dependencies:**
   ```bash
   npm install
   ```

2. **Install server dependencies:**
   ```bash
   cd Techrypt_sourcecode/server
   npm install
   ```

3. **Install React frontend dependencies:**
   ```bash
   cd Techrypt_sourcecode/Techrypt
   npm install
   ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Environment Setup

1. **Server Environment** - Create `Techrypt_sourcecode/server/.env`:
   ```env
   PORT=5000
   MONGODB_URI=your_mongodb_connection_string
   JWT_SECRET=your_jwt_secret
   ADMIN_EMAIL=your_admin_email
   ADMIN_PASSWORD=your_admin_password
   EMAIL_USER=your_email
   EMAIL_PASS=your_email_password
   ```

2. **Frontend Environment** - Create `Techrypt_sourcecode/Techrypt/.env`:
   ```env
   VITE_EMAILJS_SERVICE_ID=your_service_id
   VITE_EMAILJS_TEMPLATE_ID=your_template_id
   VITE_EMAILJS_PUBLIC_KEY=your_public_key
   REACT_APP_API_URL=http://localhost:5001
   REACT_APP_BACKEND_URL=http://localhost:5000
   REACT_APP_CHATBOT_ENABLED=true
   VITE_GA4_MEASUREMENT_ID=your_ga4_id
   ```

### Running the Application

```bash
npm run dev
```

This starts:
- Node.js server on port 5000
- React frontend on port 5173 (Vite default)
- Python chatbot on port 5001

### Individual Services

- **Start only server:** `npm run start:node`
- **Start only frontend:** `npm run start:react`
- **Start only chatbot:** `npm run start:python`
- **Build for production:** `npm run build`

### Dependencies Overview

#### Server Dependencies
- **express** - Web framework
- **mongoose** - MongoDB ODM
- **cors** - Cross-origin resource sharing
- **dotenv** - Environment variables
- **axios** - HTTP client
- **bcrypt** - Password hashing
- **jsonwebtoken** - JWT authentication
- **nodemailer** - Email sending
- **multer** - File upload handling
- **node-cron** - Task scheduling

#### Frontend Dependencies
- **react** - UI library
- **vite** - Build tool
- **react-router-dom** - Routing
- **axios** - HTTP client
- **framer-motion** - Animations
- **tailwindcss** - CSS framework
- **lucide-react** - Icons
- **react-toastify** - Notifications
- **swiper** - Carousel/slider

#### Python Dependencies
- **flask** - Web framework
- **transformers** - AI/ML models
- **torch** - Deep learning
- **numpy** - Numerical computing
- **pandas** - Data manipulation
- **pymongo** - MongoDB driver
- **flask-cors** - CORS for Flask

### Troubleshooting

1. **Port conflicts:** Change ports in .env files
2. **Python not found:** Ensure Python is in PATH
3. **Dependencies missing:** Run `npm run setup` again
4. **MongoDB connection:** Check MONGODB_URI in .env
5. **CORS issues:** Verify frontend/backend URLs match

### Adding New Dependencies

- **Node.js server:** Add to `Techrypt_sourcecode/server/package.json`
- **React frontend:** Add to `Techrypt_sourcecode/Techrypt/package.json`
- **Python chatbot:** Add to `requirements.txt`
- **Development tools:** Add to root `package.json` devDependencies
