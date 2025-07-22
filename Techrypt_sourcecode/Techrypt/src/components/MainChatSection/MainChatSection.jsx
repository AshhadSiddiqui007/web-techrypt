import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaRobot, FaPaperPlane, FaUser } from 'react-icons/fa';

const MainChatSection = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "👋 Hello! I'm your intelligent assistant from Techrypt. I can help you explore our digital services and find the perfect solution for your business. What type of business do you have?",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

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
      // Call the multi-tenant chatbot with techrypt profile
      const response = await fetch(`${import.meta.env.VITE_FLASK_BACKEND}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue,
          user_context: {
            business_profile: 'techrypt',
            domain: 'techrypt.com',
            source: 'main_page_chat',
            conversation_context: messages.length > 1 ? 'continuing' : 'first_message'
          }
        })
      });

      const data = await response.json();
      
      setTimeout(() => {
        // Format the response text
        const formattedResponse = formatChatResponse(data.response || "I'm here to help you grow your business with our digital solutions! What specific challenge can I help you overcome?");
        
        const botMessage = {
          id: Date.now() + 1,
          text: formattedResponse,
          sender: 'bot',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, botMessage]);
        setIsTyping(false);
      }, 1000);

    } catch (error) {
      console.error('Chat error:', error);
      setTimeout(() => {
        const errorMessage = {
          id: Date.now() + 1,
          text: "I'm having a small technical hiccup! But I'm still here to help you transform your business with our digital solutions. What can I help you with today?",
          sender: 'bot',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, errorMessage]);
        setIsTyping(false);
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
    "Tell me about your services",
    "How can you help my business?", 
    "I need a website",
    "Show me your pricing"
  ];

  const handleQuickQuestion = (question) => {
    setInputValue(question);
  };

  return (
    <section className="py-20 bg-gradient-to-br from-[#0f0f0f] via-[#181818] to-[#1a1a1a] relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0">
        <motion.div 
          className="absolute top-20 left-10 w-72 h-72 bg-[#C4D322]/5 rounded-full blur-3xl"
          animate={{
            x: [0, 50, -30, 0],
            y: [0, -30, 20, 0],
            scale: [1, 1.2, 0.8, 1],
          }}
          transition={{
            duration: 12,
            repeat: Infinity,
            repeatType: "reverse"
          }}
        />
        <motion.div 
          className="absolute bottom-20 right-10 w-96 h-96 bg-[#C4D322]/3 rounded-full blur-3xl"
          animate={{
            x: [0, -40, 60, 0],
            y: [0, 40, -20, 0],
            scale: [1, 0.7, 1.3, 1],
          }}
          transition={{
            duration: 15,
            repeat: Infinity,
            repeatType: "reverse"
          }}
        />
      </div>

      <div className="container mx-auto px-6 relative z-10">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <motion.h2 
            className="text-4xl md:text-5xl font-bold text-white mb-6"
            initial={{ opacity: 0, scale: 0.5 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, type: "spring", stiffness: 100 }}
          >
            Chat with Our{' '}
            <motion.span 
              className="text-transparent bg-clip-text bg-gradient-to-r from-[#C4D322] to-[#A8B91A]"
              initial={{ opacity: 0, rotateY: 90 }}
              whileInView={{ opacity: 1, rotateY: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3, duration: 0.8, type: "spring", stiffness: 80 }}
            >
              AI Assistant
            </motion.span>
          </motion.h2>
          <motion.p 
            className="text-xl text-gray-300 max-w-3xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.5, duration: 0.6 }}
          >
            Get instant answers about our services, pricing, and how we can help transform your business.
          </motion.p>
        </motion.div>

        {/* Chat Interface */}
        <motion.div
          initial={{ opacity: 0, y: 60 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="max-w-4xl mx-auto"
        >
          <div className="bg-gradient-to-br from-black/90 to-black/70 rounded-3xl border border-[#C4D322]/20 backdrop-blur-sm overflow-hidden shadow-2xl">
            {/* Chat Header */}
            <div className="bg-gradient-to-r from-black to-[#C4D322]/20 p-6 border-b border-[#C4D322]/20">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-gradient-to-br from-[#C4D322] to-[#A8B91A] rounded-full flex items-center justify-center">
                  <FaRobot className="text-black text-xl" />
                </div>
                <div>
                  <h3 className="text-white font-semibold text-lg">Techrypt AI Assistant</h3>
                  <p className="text-gray-300 text-sm">Ready to help grow your business</p>
                </div>
                <div className="ml-auto">
                  <div className="w-3 h-3 bg-[#C4D322] rounded-full animate-pulse"></div>
                </div>
              </div>
            </div>

            {/* Messages Area */}
            <div className="h-96 overflow-y-auto p-6 space-y-6 bg-gradient-to-b from-black/50 to-black/80">
              <AnimatePresence>
                {messages.map((message) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`max-w-[80%] ${
                      message.sender === 'user' 
                        ? 'bg-gradient-to-r from-[#C4D322] to-[#A8B91A] text-black' 
                        : 'bg-black/60 text-gray-100 border border-[#C4D322]/20'
                    } rounded-2xl p-4 shadow-lg`}>
                      <div className="flex items-start space-x-3">
                        {message.sender === 'bot' && (
                          <FaRobot className="text-[#C4D322] mt-1 flex-shrink-0" />
                        )}
                        {message.sender === 'user' && (
                          <FaUser className="text-black/80 mt-1 flex-shrink-0" />
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
                  <div className="bg-black/60 border border-[#C4D322]/20 rounded-2xl p-4 flex items-center space-x-3">
                    <FaRobot className="text-[#C4D322]" />
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-[#C4D322] rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-[#C4D322] rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-[#C4D322] rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                  </div>
                </motion.div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Quick Questions */}
            {messages.length === 1 && (
              <div className="px-6 py-4 bg-black/30 border-t border-[#C4D322]/20">
                <div className="text-xs text-gray-400 mb-3">Quick questions:</div>
                <div className="flex flex-wrap gap-2">
                  {quickQuestions.map((question, index) => (
                    <button
                      key={index}
                      onClick={() => handleQuickQuestion(question)}
                      className="bg-[#C4D322]/20 hover:bg-[#C4D322]/30 text-[#C4D322] text-xs px-3 py-2 rounded-full border border-[#C4D322]/30 transition-all duration-200 hover:border-[#C4D322]/50 hover:scale-105"
                    >
                      {question}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Input Area */}
            <div className="p-6 bg-black/40 border-t border-[#C4D322]/20">
              <div className="flex items-end space-x-4">
                <div className="flex-1 relative">
                  <textarea
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask about our services, pricing, or how we can help your business..."
                    className="w-full bg-black/60 text-white placeholder-gray-400 rounded-xl p-4 pr-12 border border-[#C4D322]/30 focus:border-[#C4D322] focus:outline-none resize-none min-h-[50px] max-h-[120px]"
                    rows="1"
                  />
                </div>
                <button
                  onClick={sendMessage}
                  disabled={!inputValue.trim()}
                  className="bg-gradient-to-r from-[#C4D322] to-[#A8B91A] hover:from-[#A8B91A] hover:to-[#C4D322] disabled:from-gray-600 disabled:to-gray-600 disabled:cursor-not-allowed text-black font-semibold p-4 rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl hover:scale-105 disabled:hover:scale-100"
                >
                  <FaPaperPlane className="text-sm" />
                </button>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="text-center mt-12"
        >
          <p className="text-white text-sm">
            Need more detailed assistance? Our team is ready to help you personally.
          </p>
          <motion.button
            className="mt-4 px-6 py-3 bg-gradient-to-r from-[#C4D322] to-[#A8B91A] text-black font-semibold rounded-lg hover:shadow-xl hover:shadow-[#C4D322]/20 transition-all duration-300"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => {
              // Trigger the main chatbot to open
              const event = new CustomEvent('openTechryptChatbot', {
                detail: {
                  contextMessage: "I'd like to schedule a consultation to discuss my business needs in detail.",
                  businessType: 'Consultation Request',
                  showAppointmentForm: true
                }
              });
              window.dispatchEvent(event);
            }}
          >
            Book a Free Consultation
          </motion.button>
        </motion.div>
      </div>
    </section>
  );
};

export default MainChatSection;