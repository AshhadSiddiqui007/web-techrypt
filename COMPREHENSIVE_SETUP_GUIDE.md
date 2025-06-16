# 🚀 Techrypt Chatbot - Comprehensive Setup Guide

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Project Overview](#project-overview)
3. [Backend Setup (Python/Flask)](#backend-setup)
4. [Frontend Setup (React/Vite)](#frontend-setup)
5. [Database Setup (MongoDB)](#database-setup)
6. [Environment Configuration](#environment-configuration)
7. [Integration & Testing](#integration--testing)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

---

## 🖥️ System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, or Linux Ubuntu 18.04+
- **RAM**: 8GB (16GB recommended for AI features)
- **Storage**: 5GB free space
- **Internet**: Stable connection for package downloads

### Software Requirements
- **Python**: 3.8+ (3.9+ recommended)
- **Node.js**: 18.0+ (20.0+ recommended)
- **Git**: Latest version
- **MongoDB**: 6.0+ (local or Atlas)

---

## 🏗️ Project Overview

The Techrypt Chatbot consists of three main components:

```
techrypt-chatbot/
├── 📁 Backend (Python/Flask)
│   ├── smart_llm_chatbot.py      # Main chatbot server
│   ├── data.csv                  # Training data
│   ├── techrypt_business_api.py  # Business API integration
│   └── enhanced_business_intelligence.py
├── 📁 Frontend (React/Vite)
│   └── Techrypt_sourcecode/Techrypt/
│       ├── src/                  # React components
│       ├── package.json          # Dependencies
│       └── vite.config.js        # Build configuration
└── 📁 Database (MongoDB)
    ├── Appointments collection
    ├── Users collection
    └── Conversations collection
```

---

## 🐍 Backend Setup (Python/Flask)

### Step 1: Clone Repository
```bash
git clone https://github.com/Feynman-0/web-techrypt.git
cd web-techrypt
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies
```bash
# Core dependencies
pip install flask flask-cors pandas pymongo requests openpyxl python-dateutil

# AI/ML dependencies (optional but recommended)
pip install torch transformers sentence-transformers scikit-learn numpy

# Additional utilities
pip install python-dotenv schedule smtplib
```

### Step 4: Verify CSV Data File
Ensure `data.csv` exists in the root directory with the following structure:
```csv
user_message,business_type,intent,response
"What payment methods can you integrate?","general","service_inquiry","Great choice! Payment gateway integration includes:..."
```

### Step 5: Start Backend Server
```bash
python smart_llm_chatbot.py
```

**Expected Output:**
```
🤖 ENHANCED INTELLIGENT LLM CHATBOT SERVER
✅ CSV training data loaded: 479 rows
🚀 Starting Enhanced Chatbot Server...
📡 Server: http://localhost:5000
```

---

## ⚛️ Frontend Setup (React/Vite)

### Step 1: Navigate to Frontend Directory
```bash
cd Techrypt_sourcecode/Techrypt
```

### Step 2: Install Node.js Dependencies
```bash
# Using npm
npm install

# Or using yarn
yarn install
```

### Step 3: Verify Package.json Dependencies
Key dependencies should include:
```json
{
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "axios": "^1.6.0",
    "react-router-dom": "^6.26.2",
    "framer-motion": "^11.18.2",
    "@tailwindcss/vite": "^4.1.4"
  }
}
```

### Step 4: Start Development Server
```bash
# Development mode
npm run dev

# Or using yarn
yarn dev
```

**Expected Output:**
```
  VITE v5.4.19  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

---

## 🗄️ Database Setup (MongoDB)

### Option A: MongoDB Atlas (Cloud - Recommended)

1. **Create Atlas Account**
   - Visit [MongoDB Atlas](https://www.mongodb.com/atlas)
   - Sign up for free account

2. **Create Cluster**
   - Choose "Build a Database"
   - Select "M0 Sandbox" (Free tier)
   - Choose your preferred region

3. **Configure Access**
   - Add your IP address to whitelist
   - Create database user with read/write permissions

4. **Get Connection String**
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/techrypt_db
   ```

### Option B: Local MongoDB Installation

#### Windows:
```powershell
# Using Chocolatey
choco install mongodb

# Or download from MongoDB website
# https://www.mongodb.com/try/download/community
```

#### macOS:
```bash
# Using Homebrew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

#### Linux (Ubuntu):
```bash
# Import MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Install MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB service
sudo systemctl start mongod
sudo systemctl enable mongod
```

---

## ⚙️ Environment Configuration

### Backend Environment Variables
Create `.env` file in root directory:
```env
# Database Configuration
MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/techrypt_db
DATABASE_NAME=techrypt_db

# API Configuration
USE_TINYLLAMA=false
USE_BUSINESS_API=true
INTELLIGENT_MODE=true
CSV_DATA_PATH=data.csv

# Email Configuration (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# External API Keys (Optional)
HUGGINGFACE_API_KEY=your-huggingface-key
OPENAI_API_KEY=your-openai-key
```

### Frontend Environment Variables
Create `.env` file in `Techrypt_sourcecode/Techrypt/`:
```env
# Backend API URL
VITE_API_URL=http://localhost:5000

# EmailJS Configuration (Optional)
VITE_EMAILJS_SERVICE_ID=your-service-id
VITE_EMAILJS_TEMPLATE_ID=your-template-id
VITE_EMAILJS_PUBLIC_KEY=your-public-key

# Calendly Integration (Optional)
VITE_CALENDLY_URL=https://calendly.com/your-username
```

---

## 🔗 Integration & Testing

### Step 1: Start Both Servers
```bash
# Terminal 1: Backend
python smart_llm_chatbot.py

# Terminal 2: Frontend
cd Techrypt_sourcecode/Techrypt
npm run dev
```

### Step 2: Test Backend API
```bash
# Test health endpoint
curl http://localhost:5000/health

# Test chat endpoint
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_name": "Test", "user_context": {"session_id": "test"}}'
```

### Step 3: Test Frontend-Backend Integration
1. Open browser to `http://localhost:5173`
2. Open chatbot widget
3. Send test message: "What payment methods can you integrate?"
4. Verify response comes from CSV data with source `csv_priority_match`

### Step 4: Test Database Connection
```bash
# Run database test script
python test_mongodb_setup.py
```

---

## 🚀 Deployment

### Production Build

#### Frontend:
```bash
cd Techrypt_sourcecode/Techrypt
npm run build
```

#### Backend:
```bash
# Install production WSGI server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 smart_llm_chatbot:app
```

### Environment-Specific Configurations

#### Development:
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:5000`
- Database: Local MongoDB or Atlas

#### Production:
- Frontend: Served via CDN/Static hosting
- Backend: Deployed on cloud platform (AWS, Heroku, etc.)
- Database: MongoDB Atlas (recommended)

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip list | grep flask

# Check port availability
netstat -an | grep 5000
```

#### 2. Frontend Build Errors
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node.js version
node --version  # Should be 18.0+
```

#### 3. Database Connection Issues
```bash
# Test MongoDB connection
python -c "import pymongo; print('MongoDB connection OK')"

# Check MongoDB service status (local)
# Windows: services.msc -> MongoDB
# macOS: brew services list | grep mongodb
# Linux: sudo systemctl status mongod
```

#### 4. CORS Issues
Ensure Flask-CORS is properly configured:
```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])
```

#### 5. CSV Data Not Loading
```bash
# Verify CSV file exists and has correct format
python -c "import pandas as pd; print(pd.read_csv('data.csv').head())"
```

### Performance Optimization

#### Backend:
- Disable TinyLLaMA for faster startup: `USE_TINYLLAMA=false`
- Use production WSGI server: Gunicorn or uWSGI
- Enable response caching
- Optimize CSV data loading

#### Frontend:
- Use production build: `npm run build`
- Enable gzip compression
- Optimize images and assets
- Implement lazy loading

### Monitoring & Logs

#### Backend Logs:
```bash
# View real-time logs
tail -f smart_llm_chatbot.log

# Check specific errors
grep "ERROR" smart_llm_chatbot.log
```

#### Frontend Logs:
- Open browser Developer Tools (F12)
- Check Console tab for JavaScript errors
- Check Network tab for API call issues

---

## 📞 Support

For additional support:
1. Check existing documentation files in the repository
2. Review GitHub Issues
3. Contact the development team

---

---

## 🧪 Advanced Configuration

### AI Features Setup (Optional)

#### TinyLLaMA Integration:
```bash
# Install PyTorch (CPU version)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install Transformers
pip install transformers accelerate

# Enable in environment
USE_TINYLLAMA=true
```

#### Sentence Transformers:
```bash
# Install sentence transformers
pip install sentence-transformers

# This enables enhanced CSV similarity matching
```

### Email Integration Setup

#### Gmail SMTP Configuration:
1. Enable 2-Factor Authentication on Gmail
2. Generate App Password:
   - Google Account → Security → App passwords
   - Select "Mail" and generate password
3. Update `.env`:
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASSWORD=your-16-char-app-password
   ```

#### EmailJS Frontend Setup:
1. Create account at [EmailJS](https://www.emailjs.com/)
2. Create email service and template
3. Update frontend `.env`:
   ```env
   VITE_EMAILJS_SERVICE_ID=service_xxxxxxx
   VITE_EMAILJS_TEMPLATE_ID=template_xxxxxxx
   VITE_EMAILJS_PUBLIC_KEY=your-public-key
   ```

### Automated Export System

#### Weekly Export Setup:
```bash
# Install additional dependencies
pip install schedule

# Configure automated exports
python setup_automated_export.py

# Start export service
python automated_weekly_export.py
```

---

## 📊 Data Management

### CSV Training Data Format
The `data.csv` file should follow this exact structure:

```csv
user_message,business_type,intent,response
"What payment methods can you integrate?","general","service_inquiry","Great choice{name}! Payment gateway integration includes:

• Stripe integration
• PayPal processing
• Square payments
• Razorpay support
• Secure transactions

Ready to discuss your payment needs?"
```

**Important Notes:**
- Use `{name}` placeholder for personalization
- Format responses with bullet points (•)
- Keep responses concise but informative
- Include call-to-action questions

### Database Collections Structure

#### Appointments Collection:
```javascript
{
  "_id": ObjectId,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "business_type": "restaurant",
  "services_interested": ["website", "social_media"],
  "preferred_date": "2024-01-15",
  "preferred_time": "10:00 AM",
  "message": "Need help with online presence",
  "status": "pending",
  "timestamp": ISODate,
  "session_id": "session_123"
}
```

#### Users Collection:
```javascript
{
  "_id": ObjectId,
  "name": "Jane Smith",
  "email": "jane@example.com",
  "business_type": "retail",
  "first_interaction": ISODate,
  "last_interaction": ISODate,
  "total_sessions": 3,
  "services_discussed": ["website", "branding"]
}
```

#### Conversations Collection:
```javascript
{
  "_id": ObjectId,
  "session_id": "session_123",
  "user_message": "What services do you offer?",
  "bot_response": "Great question! We offer...",
  "timestamp": ISODate,
  "source": "csv_priority_match",
  "confidence": 0.95,
  "business_type": "general"
}
```

---

## 🔒 Security Best Practices

### Environment Security:
- Never commit `.env` files to version control
- Use strong passwords for database access
- Rotate API keys regularly
- Enable MongoDB authentication

### API Security:
```python
# Add rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    # Chat endpoint logic
```

### CORS Configuration:
```python
# Production CORS setup
CORS(app, origins=[
    "https://yourdomain.com",
    "https://www.yourdomain.com"
])
```

---

## 📈 Performance Monitoring

### Backend Monitoring:
```python
# Add performance logging
import time
import logging

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - g.start_time
    logging.info(f"Request took {duration:.3f}s")
    return response
```

### Frontend Performance:
```javascript
// Add performance monitoring
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log(`${entry.name}: ${entry.duration}ms`);
  }
});
observer.observe({entryTypes: ['navigation', 'resource']});
```

---

## 🚀 Quick Start Scripts

### Windows Batch Scripts:

#### `start_backend.bat`:
```batch
@echo off
echo Starting Techrypt Backend...
cd /d "%~dp0"
call venv\Scripts\activate
python smart_llm_chatbot.py
pause
```

#### `start_frontend.bat`:
```batch
@echo off
echo Starting Techrypt Frontend...
cd /d "%~dp0\Techrypt_sourcecode\Techrypt"
npm run dev
pause
```

#### `start_both.bat`:
```batch
@echo off
echo Starting Techrypt Full Stack...
start cmd /k "call start_backend.bat"
timeout /t 5
start cmd /k "call start_frontend.bat"
echo Both servers starting...
echo Frontend: http://localhost:5173
echo Backend: http://localhost:5000
pause
```

### PowerShell Scripts:

#### `start_both.ps1`:
```powershell
Write-Host "🚀 Starting Techrypt Chatbot System..." -ForegroundColor Green

# Start Backend
Write-Host "📡 Starting Backend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {Set-Location '$PWD'; .\venv\Scripts\Activate.ps1; python smart_llm_chatbot.py}"

# Wait for backend to start
Start-Sleep -Seconds 5

# Start Frontend
Write-Host "⚛️ Starting Frontend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {Set-Location '$PWD\Techrypt_sourcecode\Techrypt'; npm run dev}"

Write-Host "✅ Both servers are starting..." -ForegroundColor Green
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "Backend: http://localhost:5000" -ForegroundColor Cyan
```

---

**🎉 Congratulations! Your Techrypt Chatbot should now be fully operational.**

Test the complete system by sending a message through the frontend and verifying it reaches the backend and returns appropriate responses from the CSV data.

For ongoing maintenance, refer to the monitoring sections and keep dependencies updated regularly.
