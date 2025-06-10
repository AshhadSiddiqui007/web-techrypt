import React, { useState, useEffect, useRef } from 'react';
import './TechryptChatbot.css';
import { BsRobot, BsPerson, BsSend, BsMic, BsMicMute, BsVolumeUp, BsX, BsDash } from 'react-icons/bs';

const SmartChatbot = ({ isOpen, onClose }) => {
  // Enhanced state management for ChatGPT-like experience
  const [messages, setMessages] = useState(() => loadMessages());
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [userContext, setUserContext] = useState({
    name: '',
    email: '',
    phone: '',
    businessType: '',
    servicesDiscussed: [],
    appointmentIntent: false
  });
  
  // Form states for intelligent form handling
  const [showContactForm, setShowContactForm] = useState(false);
  const [showAppointmentForm, setShowAppointmentForm] = useState(false);
  const [contactFormData, setContactFormData] = useState({ name: '', email: '', phone: '' });
  const [appointmentFormData, setAppointmentFormData] = useState({
    name: '',
    email: '',
    phone: '',
    services: [],
    date: '',
    time: '',
    notes: ''
  });

  const messagesEndRef = useRef(null);

  // Load messages with intelligent persistence
  function loadMessages() {
    try {
      const isPageReload = !sessionStorage.getItem('techrypt-session-active');
      
      if (isPageReload) {
        localStorage.removeItem('techrypt-chat-messages');
        sessionStorage.setItem('techrypt-session-active', 'true');
        return [{
          id: 1,
          text: "Hello! I'm your intelligent assistant from Techrypt. I'm here to help you grow your business with our digital services. What type of business do you have?",
          sender: 'bot',
          timestamp: new Date(),
          showContactForm: true
        }];
      } else {
        const savedMessages = localStorage.getItem('techrypt-chat-messages');
        if (savedMessages) {
          return JSON.parse(savedMessages).map(msg => ({
            ...msg,
            timestamp: new Date(msg.timestamp)
          }));
        }
      }
    } catch (error) {
      console.log('Error loading chat history:', error);
    }
    
    return [{
      id: 1,
      text: "Hello! I'm your intelligent assistant from Techrypt. How can I help you grow your business today?",
      sender: 'bot',
      timestamp: new Date()
    }];
  }

  // Auto-scroll with smooth behavior
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Save messages with intelligent caching
  useEffect(() => {
    try {
      localStorage.setItem('techrypt-chat-messages', JSON.stringify(messages));
    } catch (error) {
      console.log('Error saving chat history:', error);
    }
  }, [messages]);

  // Intelligent contact form display
  useEffect(() => {
    if (isOpen && !userContext.email) {
      const timer = setTimeout(() => {
        setShowContactForm(true);
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, [isOpen, userContext.email]);

  // Enhanced voice recognition
  const startListening = () => {
    if ('webkitSpeechRecognition' in window) {
      const recognition = new window.webkitSpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInputMessage(transcript);
        setIsListening(false);
        // Auto-send voice messages for better UX
        setTimeout(() => sendMessage(transcript), 500);
      };

      recognition.onerror = () => {
        setIsListening(false);
      };

      recognition.onend = () => setIsListening(false);

      setIsListening(true);
      recognition.start();
    }
  };

  // Intelligent message sending with context awareness
  const sendMessage = async (messageText = inputMessage) => {
    if (!messageText.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: messageText,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Send to intelligent AI backend
      const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageText,
          user_name: userContext.name || '',
          user_context: userContext
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();

      // Create intelligent bot response
      const botMessage = {
        id: Date.now() + 1,
        text: data.response || getIntelligentFallback(messageText),
        sender: 'bot',
        timestamp: new Date(),
        showContactForm: data.show_contact_form,
        showAppointmentForm: data.show_appointment_form
      };

      setMessages(prev => [...prev, botMessage]);

      // Update user context intelligently
      updateUserContext(messageText, data);

      // Handle intelligent form triggers
      handleIntelligentFormTriggers(messageText, data);

    } catch (error) {
      console.log('AI backend error:', error.message);
      
      const botMessage = {
        id: Date.now() + 1,
        text: getIntelligentFallback(messageText),
        sender: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Intelligent context updating
  const updateUserContext = (message, aiResponse) => {
    const emailRegex = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/;
    const phoneRegex = /(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}/;
    
    setUserContext(prev => {
      const updated = { ...prev };
      
      // Extract email
      const emailMatch = message.match(emailRegex);
      if (emailMatch) updated.email = emailMatch[0];
      
      // Extract phone
      const phoneMatch = message.match(phoneRegex);
      if (phoneMatch) updated.phone = phoneMatch[0];
      
      // Detect business type
      if (aiResponse.business_type) {
        updated.businessType = aiResponse.business_type;
      }
      
      // Track appointment intent
      const appointmentKeywords = ['appointment', 'schedule', 'book', 'meeting', 'consultation'];
      if (appointmentKeywords.some(keyword => message.toLowerCase().includes(keyword))) {
        updated.appointmentIntent = true;
      }
      
      return updated;
    });
  };

  // Intelligent form trigger handling
  const handleIntelligentFormTriggers = (message, aiResponse) => {
    // Show contact form intelligently
    if (aiResponse.show_contact_form || (!userContext.email && shouldShowContactForm(message))) {
      setTimeout(() => setShowContactForm(true), 1000);
    }
    
    // Show appointment form intelligently
    if (aiResponse.show_appointment_form || shouldShowAppointmentForm(message)) {
      setTimeout(() => {
        setAppointmentFormData(prev => ({
          ...prev,
          name: userContext.name,
          email: userContext.email,
          phone: userContext.phone
        }));
        setShowAppointmentForm(true);
      }, 1000);
    }
  };

  // Intelligent contact form detection
  const shouldShowContactForm = (message) => {
    const triggers = ['contact', 'email', 'phone', 'call me', 'reach out', 'get in touch'];
    return triggers.some(trigger => message.toLowerCase().includes(trigger));
  };

  // Intelligent appointment form detection
  const shouldShowAppointmentForm = (message) => {
    const triggers = [
      'schedule', 'book', 'appointment', 'meeting', 'consultation',
      'call', 'demo', 'yes please', 'sure', 'excellent', 'perfect'
    ];
    return triggers.some(trigger => message.toLowerCase().includes(trigger));
  };

  // Intelligent fallback responses
  const getIntelligentFallback = (message) => {
    const msg = message.toLowerCase();
    
    // Business-specific responses
    if (msg.includes('business') || msg.includes('company')) {
      return `Great! I'd love to learn more about your business. Techrypt specializes in helping businesses grow through:

🌐 Website Development - Professional online presence
📱 Social Media Marketing - Engage your customers  
🎨 Branding Services - Create memorable identity
🤖 Chatbot Development - Automate customer service
⚡ Automation Packages - Streamline operations
💳 Payment Gateway Integration - Secure transactions

What type of business do you have?`;
    }
    
    // Service inquiries
    if (msg.includes('service') || msg.includes('help')) {
      return `I'm here to help you grow your business! Our main services include:

1. Website Development
2. Social Media Marketing
3. Branding Services
4. Chatbot Development
5. Automation Packages
6. Payment Gateway Integration

Which service interests you most, or would you like to schedule a consultation to discuss your specific needs?`;
    }
    
    // Default intelligent response
    return `Thank you for your message! I'm here to help you grow your business with Techrypt's digital services. Could you tell me more about what you're looking for, or would you like to schedule a consultation to discuss your needs?`;
  };

  // Minimize/maximize functionality
  const toggleMinimize = () => {
    setIsMinimized(!isMinimized);
  };

  return (
    <>
      {/* Transparent overlay background */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-20 z-40"
          onClick={onClose}
        />
      )}
      
      {/* Smart Chatbot Container */}
      <div className={`smart-chatbot-container ${isOpen ? 'open' : 'closed'} ${isMinimized ? 'minimized' : ''}`}>
        {/* Header with green theme */}
        <div className="chatbot-header bg-green-600">
          <div className="flex items-center">
            <BsRobot className="text-white text-xl mr-2" />
            <span className="text-white font-semibold">Techrypt Assistant</span>
          </div>
          <div className="flex items-center space-x-2">
            <button 
              onClick={toggleMinimize}
              className="text-white hover:bg-green-700 p-1 rounded"
            >
              <BsDash />
            </button>
            <button 
              onClick={onClose}
              className="text-white hover:bg-green-700 p-1 rounded"
            >
              <BsX />
            </button>
          </div>
        </div>

        {/* Messages Area */}
        {!isMinimized && (
          <>
            <div className="messages-container">
              {messages.map((message) => (
                <div key={message.id} className={`message ${message.sender}`}>
                  <div className="message-content">
                    <div className="message-avatar">
                      {message.sender === 'bot' ? <BsRobot /> : <BsPerson />}
                    </div>
                    <div className="message-text">
                      {message.text}
                    </div>
                  </div>
                </div>
              ))}
              
              {isLoading && (
                <div className="message bot">
                  <div className="message-content">
                    <div className="message-avatar">
                      <BsRobot />
                    </div>
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="input-container">
              <div className="input-wrapper">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                  placeholder="Type your message..."
                  className="message-input"
                />
                <button
                  onClick={startListening}
                  className={`voice-button ${isListening ? 'listening' : ''}`}
                  title="Voice input"
                >
                  {isListening ? <BsMicMute /> : <BsMic />}
                </button>
                <button
                  onClick={() => sendMessage()}
                  className="send-button bg-green-600 hover:bg-green-700"
                  disabled={!inputMessage.trim() || isLoading}
                >
                  <BsSend />
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </>
  );
};

export default SmartChatbot;
