# 🚀 Techrypt AI-Powered Business Consultation Chatbot

A sophisticated React-based chatbot with Flask backend featuring LLM-powered business intelligence, contextual understanding, and comprehensive service consultation capabilities.

## ✨ Features

### 🧠 **LLM-Powered Intelligence**
- **Contextual Business Understanding**: Recognizes business types from natural language descriptions
- **Regional Business Intelligence**: Understands regional terms (karyana shops, bodegas, etc.)
- **Technical Level Adaptation**: Adjusts language complexity based on user sophistication
- **True AI Responses**: LLM-generated responses with contextual understanding flags

### 💼 **Comprehensive Service Information**
- **6 Core Digital Services**: Website Development, Social Media Marketing, Branding, Chatbot Development, Automation, Payment Integration
- **Detailed Service Explanations**: Timeline, pricing, features, and benefits for each service
- **Business-Specific Recommendations**: Tailored service suggestions based on business type
- **Interactive Service Discussion**: Users can ask detailed questions about any service

### 🎯 **Advanced Business Consultation**
- **Personalized Responses**: Uses customer names and business context
- **Appointment Scheduling**: Integrated booking system with calendar management
- **Multi-Language Support**: Handles colloquial and technical business terminology
- **Performance Optimized**: Sub-3-second response times

### 🔧 **Technical Architecture**
- **React Frontend**: Modern, responsive UI with real-time chat interface
- **Flask Backend**: Python-based API with LLM integration
- **MongoDB Integration**: Conversation storage and analytics
- **Excel Export**: Appointment and lead management
- **Content Filtering**: Prohibited business detection and handling

## 🏗️ **Project Structure**

```
techcrypt_bot/
├── Techrypt_sourcecode/Techrypt/          # React Frontend
│   ├── src/
│   │   ├── components/TechryptChatbot/    # Main chatbot component
│   │   ├── components/BusinessVerticals/   # Business integration
│   │   └── src/                           # Flask Backend
│   │       ├── flask_api_server.py        # Main API server
│   │       ├── optimized_ai_backend.py    # LLM intelligence engine
│   │       └── test_llm_intelligence.py   # Intelligence validation
├── IMG/                                   # Project images and assets
├── README.md                              # This file
└── package.json                           # Node.js dependencies
```

## 🚀 **Quick Start**

### Prerequisites
- Node.js 18+ (portable version recommended)
- Python 3.8+
- MongoDB (optional, for data persistence)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/techrypt-ai-chatbot.git
cd techrypt-ai-chatbot
```

2. **Install Frontend Dependencies**
```bash
cd Techrypt_sourcecode/Techrypt
npm install
```

3. **Install Backend Dependencies**
```bash
cd src
pip install flask flask-cors requests pymongo pandas
```

4. **Start the Application**

**Backend (Terminal 1):**
```bash
cd Techrypt_sourcecode/Techrypt/src
python flask_api_server.py
```

**Frontend (Terminal 2):**
```bash
cd Techrypt_sourcecode/Techrypt
npm run dev
```

5. **Access the Application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000
- Health Check: http://localhost:5000/api/health

## 🎯 **Usage Examples**

### Business Consultation
```
User: "I run a karyana shop in Lahore and need help online"
Bot: "Hi [Name], for your karyana shop, I recommend E-commerce Store and Payment Gateway Integration..."
```

### Service Inquiries
```
User: "What are your services?"
Bot: [Displays detailed list of 6 core services with descriptions]

User: "Tell me about website development"
Bot: [Provides comprehensive website service details with pricing and timeline]
```

### Appointment Booking
```
User: "I want to schedule a consultation"
Bot: [Opens appointment form with pre-filled contact information]
```

## 🧪 **Testing**

### LLM Intelligence Validation
```bash
cd Techrypt_sourcecode/Techrypt/src
python test_llm_intelligence.py
```

### Frontend-Backend Integration
```bash
cd Techrypt_sourcecode/Techrypt/src
python test_frontend_integration.py
```

## 📊 **Performance Metrics**

- **Response Time**: <3 seconds average
- **Business Detection Accuracy**: >80%
- **LLM Intelligence Rate**: >80% (with proper LLM integration)
- **Contextual Understanding**: Regional and technical business terms
- **Service Coverage**: 6 comprehensive digital services

## 🔧 **Configuration**

### Backend Configuration
Edit `optimized_ai_backend.py`:
```python
# LLM Configuration
LLM_PIPELINE = "ENHANCED_CONTEXTUAL_AI"  # or "GROQ_API", "HUGGINGFACE_API"
API_KEYS = {
    "GROQ_API_KEY": "your_groq_key",
    "HF_API_KEY": "your_huggingface_key"
}
```

### Frontend Configuration
Edit `TechryptChatbot.jsx`:
```javascript
// API Endpoint
const API_BASE_URL = "http://localhost:5000/api";
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Techrypt.io**: Original business consultation platform
- **React Community**: Frontend framework and components
- **Flask Community**: Backend API framework
- **LLM Providers**: Groq, Hugging Face, Together AI for AI capabilities

## 📞 **Support**

For support and questions:
- **Email**: support@techrypt.io
- **Website**: https://techrypt.io
- **Issues**: GitHub Issues page

---

**Built with ❤️ by the Techrypt Team**
