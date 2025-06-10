# Techrypt.io AI Appointment Scheduling Chatbot

A modern MERN + Flask application that combines AI-powered chatbot functionality with voice commands for seamless appointment scheduling.

## 🏗️ Architecture

- **Frontend**: React with Material-UI (Port 3000)
- **Main Backend**: Node.js/Express with MongoDB (Port 5000)
- **AI Backend**: Python/Flask with OpenAI integration (Port 5001)
- **Database**: MongoDB

## ✨ Features

### 🤖 AI Chatbot
- Natural language understanding
- Intent detection and entity extraction
- Context-aware conversations
- Fallback responses when AI services are unavailable

### 🎤 Voice Commands
- Speech-to-text using Web Speech API and OpenAI Whisper
- Text-to-speech responses
- Voice-activated appointment booking
- Multi-engine fallback support

### 📅 Appointment Management
- Real-time availability checking
- Email confirmations and reminders
- Admin dashboard for appointment management
- Multiple service categories

### 🔧 Technical Features
- CORS enabled for cross-origin requests
- Input validation and sanitization
- Error handling and logging
- Rate limiting and security headers
- Responsive Material-UI design

## 🚀 Quick Start

### Prerequisites
- Node.js (v16+)
- Python (v3.8+)
- MongoDB (local or Atlas)

### 1. Clone and Install
```bash
git clone <repository-url>
cd techcrypt_bot
npm install
```

### 2. Setup Backend Services
```bash
# Install Node.js backend dependencies
cd server
npm install
cp .env.example .env
# Edit .env with your MongoDB URI and other configs

# Install Python AI backend dependencies
cd ../ai_backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your OpenAI API key
```

### 3. Setup Frontend
```bash
cd ../client
# Dependencies already installed via root npm install
```

### 4. Configure Environment Variables

#### server/.env
```env
PORT=5000
MONGO_URI=mongodb://localhost:27017/techrypt
JWT_SECRET=your_jwt_secret_here
EMAIL_HOST=smtp.gmail.com
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
FLASK_AI_URL=http://localhost:5001
```

#### ai_backend/.env
```env
FLASK_PORT=5001
OPENAI_API_KEY=your_openai_api_key_here
CORS_ORIGINS=http://localhost:3000,http://localhost:5000
```

### 5. Start All Services
```bash
# From root directory
npm run dev
```

This starts:
- React frontend: http://localhost:3000
- Node.js backend: http://localhost:5000
- Python AI backend: http://localhost:5001

## 📋 API Endpoints

### Node.js Backend (Port 5000)
- `POST /api/appointments` - Create appointment
- `GET /api/appointments/available-slots` - Get available time slots
- `GET /api/health` - Health check
- `POST /api/admin/login` - Admin authentication
- `GET /api/admin/appointments` - List all appointments (admin)

### Python AI Backend (Port 5001)
- `POST /api/chat` - AI chat processing
- `POST /api/voice-to-text` - Speech recognition
- `POST /api/text-to-speech` - Speech synthesis
- `POST /api/intent` - Intent detection
- `GET /api/health` - Health check

## 🗄️ Database Setup

### Local MongoDB
```bash
# Install MongoDB Community Edition
# Start MongoDB service
mongod --dbpath /path/to/data/directory
```

### MongoDB Atlas (Recommended)
1. Create account at https://www.mongodb.com/atlas
2. Create cluster and get connection string
3. Add to server/.env: `MONGO_URI=mongodb+srv://...`

## 🎯 Usage Examples

### Voice Commands
- "Hello, I want to book an appointment"
- "I need web development services"
- "My name is John Doe and my email is john@example.com"
- "Schedule me for next Tuesday at 2 PM"

### Chat Examples
- "What services do you offer?"
- "How much does web development cost?"
- "I want to cancel my appointment"
- "When are you available this week?"

## 🔧 Development

### Running Individual Services

#### Node.js Backend Only
```bash
cd server
npm run dev
```

#### Python AI Backend Only
```bash
cd ai_backend
venv\Scripts\activate
python app.py
```

#### React Frontend Only
```bash
cd client
npm start
```

### Testing
```bash
# Test backend health
curl http://localhost:5000/api/health

# Test AI backend
curl http://localhost:5001/api/health

# Test chat endpoint
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

## 🛠️ Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Ensure MongoDB is running
   - Check connection string in .env
   - Verify network access

2. **Python Dependencies Error**
   - Activate virtual environment
   - Update pip: `pip install --upgrade pip`
   - Install system audio dependencies

3. **OpenAI API Errors**
   - Verify API key is correct
   - Check API quota and billing
   - App works with fallback responses without API key

4. **Voice Recognition Not Working**
   - Ensure HTTPS or localhost
   - Check browser permissions
   - Verify microphone access

5. **CORS Issues**
   - Check CORS_ORIGINS in ai_backend/.env
   - Verify CLIENT_URL in server/.env

## 📦 Production Deployment

### Environment Setup
- Set NODE_ENV=production
- Use strong JWT secrets
- Configure proper email credentials
- Use MongoDB Atlas
- Set up SSL/HTTPS
- Configure proper logging

### Docker (Optional)
```bash
docker-compose up --build
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📄 License

MIT License - see LICENSE file for details

## 📞 Support

For issues or questions:
- Check logs in `server/` and `ai_backend/logs/`
- Verify environment variables
- Ensure all services are running
- Contact: contact@techrypt.io

---

Built with ❤️ by Techrypt.io
