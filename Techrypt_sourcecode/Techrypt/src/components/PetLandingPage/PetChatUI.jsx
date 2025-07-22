import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaPaw, FaPaperPlane, FaUser } from 'react-icons/fa';

// FIX: Import TechryptChatbot for modal usage
import TechryptChatbot from '../TechryptChatbot/TechryptChatbot';

const PetChatUI = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "🐾 Hello! I'm here to help grow your pet business! Whether you run a veterinary clinic, pet grooming salon, or any pet-related service, I can help you attract more customers and streamline your operations. What type of pet business do you have?",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  // Track bot responses and appointment form
  const [botResponseCount, setBotResponseCount] = useState(1); // initial bot message
  const [chatDisabled, setChatDisabled] = useState(false);
  const [showAppointmentForm, setShowAppointmentForm] = useState(false);
  // Add state to control TechryptChatbot modal
  const [appointmentModalOpen, setAppointmentModalOpen] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Only scroll to bottom when the component first mounts or when bot sends a message
  useEffect(() => {
    if (messages.length === 1) {
      // Only scroll on initial load
      scrollToBottom();
    }
  }, []);

  const sendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    try {
      // Call our multi-tenant chatbot with pets profile
      const response = await fetch(`${import.meta.env.VITE_FLASK_BACKEND}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue,
          user_context: {
            business_profile: 'pets',
            domain: 'pets.techrypt.com',
            source: 'pet_landing_page',
            conversation_context: messages.length > 1 ? 'continuing' : 'first_message'
          }
        })
      });

      const data = await response.json();
      
      setTimeout(() => {
        // Format the response text
        const formattedResponse = formatChatResponse(data.response || "I'm here to help your pet business grow! Could you tell me more about your specific needs?");
        
        const botMessage = {
          id: Date.now() + 1,
          text: formattedResponse,
          sender: 'bot',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, botMessage]);
        setIsTyping(false);
        setBotResponseCount(prev => {
          const newCount = prev + 1;
          if (newCount >= 4) {
            setChatDisabled(true);
            setShowAppointmentForm(false);
            setAppointmentModalOpen(true); // Open main TechryptChatbot appointment modal
          }
          return newCount;
        });
        // Only scroll when bot responds
        setTimeout(() => scrollToBottom(), 100);
      }, 1000);

    } catch (error) {
      console.error('Chat error:', error);
      setTimeout(() => {
        const errorMessage = {
          id: Date.now() + 1,
          text: "I'm having a small technical hiccup! But I'm still here to help your pet business succeed. What specific challenge can I help you with?",
          sender: 'bot',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, errorMessage]);
        setIsTyping(false);
        
        // Only scroll when bot responds
        setTimeout(() => scrollToBottom(), 100);
      }, 1000);
    }
  };

  // Format chat response for better readability
  const formatChatResponse = (response) => {
    if (!response) return response;
    
    // Remove redundant greetings and clean up formatting
    let formatted = response
      .replace(/^(Hi|Hello|Hey)\s+[^,!.]*[,!.]\s*/i, '') // Remove "Hi [name]," at start
      .replace(/\n\s*\n/g, '\n') // Remove extra line breaks
      .trim();
    
    // If the response is too long, break it into paragraphs
    if (formatted.length > 200) {
      formatted = formatted
        .replace(/\. ([A-Z])/g, '.\n\n$1') // Add line breaks after sentences that start new topics
        .replace(/\n\s*\n\s*\n/g, '\n\n'); // Clean up triple line breaks
    }
    
    return formatted;
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const quickQuestions = [
    "I need a website for my vet clinic",
    "Help with pet grooming marketing", 
    "Booking system for my pet daycare",
    "Social media for my pet store"
  ];

  const handleQuickQuestion = (question) => {
    setInputValue(question);
  };

  return (
    <div className="bg-gradient-to-br from-black/90 to-black/90 rounded-2xl border border-black/50 h-[600px] flex flex-col overflow-hidden backdrop-blur-sm">
      {/* Chat Header */}
      <div className="bg-gradient-to-r from-black to-primary p-4 flex items-center space-x-3">
        <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
          <FaPaw className="text-white text-lg" />
        </div>
        <div>
          <h3 className="text-white font-semibold">PetCare Assistant</h3>
          <p className="text-white/80 text-sm">Specialized in pet businesses</p>
        </div>
        <div className="ml-auto">
          <div className="w-3 h-3 bg-primary rounded-full animate-pulse"></div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <AnimatePresence>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[85%] ${
                message.sender === 'user' 
                  ? 'bg-gradient-to-r from-black to-primary text-white' 
                  : 'bg-black text-gray-100'
              } rounded-2xl p-4 shadow-lg`}>
                <div className="flex items-start space-x-3">
                  {message.sender === 'bot' && (
                    <FaPaw className="text-primary mt-1 flex-shrink-0" />
                  )}
                  {message.sender === 'user' && (
                    <FaUser className="text-white/80 mt-1 flex-shrink-0" />
                  )}
                  <div className="flex-1">
                    {message.text.split('\n').map((paragraph, index) => (
                      <p key={index} className={`text-sm leading-relaxed ${index > 0 ? 'mt-3' : ''}`}>
                        {paragraph}
                      </p>
                    ))}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Typing Indicator */}
        {isTyping && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex justify-start"
          >
            <div className="bg-black rounded-2xl p-3 flex items-center space-x-2">
              <FaPaw className="text-primary" />
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
              </div>
            </div>
          </motion.div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Questions */}
      {messages.length === 1 && (
        <div className="px-4 pb-2">
          <div className="text-xs text-gray-400 mb-2">Quick questions:</div>
          <div className="flex flex-wrap gap-2">
            {quickQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => handleQuickQuestion(question)}
                className="bg-primary/20 hover:bg-primary/30 text-primary text-xs px-3 py-1 rounded-full border border-primary/30 transition-all duration-200 hover:border-primary/50"
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="p-4 border-t border-black/50">
        {chatDisabled ? (
          <div className="text-center text-primary font-semibold py-6">
            You've reached the maximum number of chatbot responses.<br />Please book an appointment to continue.
          </div>
        ) : (
          <div className="flex items-center space-x-3">
            <div className="flex-1 relative">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about your pet business needs..."
                className="w-full bg-black/50 text-white placeholder-gray-400 rounded-xl p-3 pr-12 border border-black/50 focus:border-primary focus:outline-none resize-none"
                rows="1"
                style={{ minHeight: '44px', maxHeight: '100px' }}
              />
            </div>
            <button
              onClick={sendMessage}
              disabled={!inputValue.trim()}
              className="bg-gradient-to-r from-black to-primary hover:from-black/90 hover:to-primary/90 disabled:from-gray-600 disabled:to-gray-600 disabled:cursor-not-allowed text-white font-semibold p-3 rounded-xl transition-all duration-200 shadow-lg"
            >
              <FaPaperPlane className="text-sm" />
            </button>
          </div>
        )}
      </div>
      {/* Main TechryptChatbot Appointment Modal (only modal, not full chat) */}
      {appointmentModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center z-50" style={{background: 'rgba(0,0,0,0.4)'}}>
          <div className="w-full max-w-xl">
            {/* Only render the appointment modal from TechryptChatbot, not the full chat UI */}
            <TechryptChatbot
              isOpen={true}
              onClose={() => setAppointmentModalOpen(false)}
              openAppointmentDirect={true}
              limitBotResponses={true}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default PetChatUI;
