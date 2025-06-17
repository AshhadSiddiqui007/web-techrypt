import React, { useState, useEffect, useRef } from 'react';
import './TechryptChatbot.css';
import { BsRobot, BsPerson, BsSend, BsVolumeUp, BsX } from 'react-icons/bs';
import calenderIcon from "/Images/chatbot/calender.svg";
import minimizeIcon from "/Images/chatbot/minimize.svg";
import binIcon from "/Images/chatbot/bin.svg";
import closeIcon from "/Images/chatbot/close.svg";

const TechryptChatbot = ({ isOpen, onClose }) => {
  // Load messages from localStorage or use default
  const loadMessages = () => {
    try {
      // Check if this is a page reload by looking for a session flag
      const isPageReload = !sessionStorage.getItem('techrypt-session-active');

      if (isPageReload) {
        // Clear chat history on page reload
        localStorage.removeItem('techrypt-chat-messages');
        // Set session flag to indicate the session is now active
        sessionStorage.setItem('techrypt-session-active', 'true');
      } else {
        // Load existing messages if not a page reload
        const savedMessages = localStorage.getItem('techrypt-chat-messages');
        if (savedMessages) {
          const parsed = JSON.parse(savedMessages);
          // Convert timestamp strings back to Date objects
          return parsed.map(msg => ({
            ...msg,
            timestamp: new Date(msg.timestamp)
          }));
        }
      }
    } catch (error) {
      console.log('Error loading chat history:', error);
    }

    // Smart welcome message with ChatGPT-like intelligence
    return [
      {
        id: 1,
        text: "Hello! I'm your intelligent assistant from Techrypt. I'm here to help you grow your business with our digital services. What type of business do you have, and how can I help you today?",
        sender: 'bot',
        timestamp: new Date(),
        showContactForm: true
      }
    ];
  };

  // Load contact data from localStorage
  const loadContactData = () => {
    try {
      const savedContactData = localStorage.getItem('techrypt-contact-data');
      if (savedContactData) {
        return JSON.parse(savedContactData);
      }
    } catch (error) {
      console.log('Error loading contact data:', error);
    }
    return { name: '', email: '', phone: '' };
  };

  // Core states
  const [messages, setMessages] = useState(() => loadMessages());
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // Form states
  const [showContactForm, setShowContactForm] = useState(false);
  const [showAppointmentForm, setShowAppointmentForm] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [contactData, setContactData] = useState(() => loadContactData());
  const [contactFormData, setContactFormData] = useState({ name: '', email: '', phone: '' }); // Fresh form data
  const [hasEnteredNameThisSession, setHasEnteredNameThisSession] = useState(false); // Track if name was entered this session
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    services: [], // Changed to array for multiple services
    date: '',
    time: '',
    notes: ''
  });
  const [contactErrors, setContactErrors] = useState({});
  const [appointmentErrors, setAppointmentErrors] = useState({});

  // Add new state variable for the thank you modal
  const [showThankYouModal, setShowThankYouModal] = useState(false);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Show contact form automatically after welcome message on first open
  useEffect(() => {
    if (isOpen) {
      // Always show contact form on first chatbot open after page load
      setTimeout(() => {
        setShowContactForm(true);
      }, 1000);
    }
  }, [isOpen]);

  // Save messages to localStorage whenever messages change
  useEffect(() => {
    try {
      localStorage.setItem('techrypt-chat-messages', JSON.stringify(messages));
    } catch (error) {
      console.log('Error saving chat history:', error);
    }
  }, [messages]);

  // Save contact data to localStorage whenever it changes
  useEffect(() => {
    try {
      localStorage.setItem('techrypt-contact-data', JSON.stringify(contactData));
    } catch (error) {
      console.log('Error saving contact data:', error);
    }
  }, [contactData]);

  // Handle page unload to clear session flag for proper reload detection
  useEffect(() => {
    const handleBeforeUnload = () => {
      // Clear session flag when page is about to unload
      sessionStorage.removeItem('techrypt-session-active');
    };

    window.addEventListener('beforeunload', handleBeforeUnload);

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, []);



  // Simple voice recognition
  const startListening = () => {
    if ('webkitSpeechRecognition' in window) {
      const recognition = new window.webkitSpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onresult = (event) => {
        setInputMessage(event.results[0][0].transcript);
        setIsListening(false);
      };

      recognition.onerror = () => {
        setIsListening(false);
        setError('Voice recognition failed');
      };

      recognition.onend = () => setIsListening(false);

      setIsListening(true);
      recognition.start();
    }
  };

  // Simple text-to-speech
  const speakText = (text) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.9;
      window.speechSynthesis.speak(utterance);
    }
  };

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
    setError(null); // Clear any previous errors

    try {
      // Try to connect to Smart AI backend with enhanced context
      const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageText,
          user_name: contactData.name || '',
          user_context: {
            name: contactData.name || '',
            email: contactData.email || '',
            phone: contactData.phone || '',
            hasEnteredNameThisSession: hasEnteredNameThisSession,
            conversationLength: messages.length
          }
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();

      // Enhanced bot message with smart features
      const botMessage = {
        id: Date.now() + 1,
        text: data.response || getFallbackResponse(messageText),
        sender: 'bot',
        timestamp: new Date(),
        showContactForm: data.show_contact_form,
        showAppointmentForm: data.show_appointment_form
      };

      setMessages(prev => [...prev, botMessage]);

      // Handle intelligent form triggers from AI response
      if (data.show_contact_form && !contactData.email) {
        setTimeout(() => setShowContactForm(true), 1000);
      }

      // ENHANCED APPOINTMENT TRIGGER - Listen for backend action flags
      const appointmentTriggers = [
        'yes', 'sure', 'alright', 'okay', 'let\'s do it', 'absolutely', 'definitely',
        'schedule appointment', 'book appointment', 'schedule meeting', 'book meeting',
        'schedule consultation', 'book consultation', 'schedule call', 'book call',
        'i want to schedule', 'i want to book', 'i need to schedule', 'i need to book',
        'can we schedule', 'can we book', 'let\'s schedule', 'let\'s book',
        'open appointment', 'appointment form', 'i\'m interested'
      ];

      const isAppointmentRequest = appointmentTriggers.some(phrase =>
        messageText.toLowerCase().includes(phrase)
      );

      // Check for backend action flag OR user appointment request
      if (data.action === 'open_form' || data.show_appointment_form || isAppointmentRequest) {
        console.log('🎯 Appointment form triggered:', {
          action: data.action,
          show_appointment_form: data.show_appointment_form,
          isAppointmentRequest
        });

        setTimeout(() => {
          setFormData(prev => ({
            ...prev,
            name: contactData.name || data.context?.name || '',
            email: contactData.email || data.context?.email || '',
            phone: contactData.phone || data.context?.phone || ''
          }));
          setShowAppointmentForm(true);
        }, 500); // Reduced delay for faster response
      }

    } catch (error) {
      console.log('AI backend error:', error.message);

      // Use fallback response
      const botMessage = {
        id: Date.now() + 1,
        text: getFallbackResponse(messageText),
        sender: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);

      // ENHANCED FALLBACK APPOINTMENT TRIGGER
      const appointmentTriggers = [
        'yes', 'sure', 'alright', 'okay', 'let\'s do it', 'absolutely', 'definitely',
        'schedule appointment', 'book appointment', 'schedule meeting', 'book meeting',
        'schedule consultation', 'book consultation', 'schedule call', 'book call',
        'i want to schedule', 'i want to book', 'i need to schedule', 'i need to book',
        'can we schedule', 'can we book', 'let\'s schedule', 'let\'s book',
        'open appointment', 'appointment form', 'i\'m interested'
      ];

      const isAppointmentRequest = appointmentTriggers.some(phrase =>
        messageText.toLowerCase().includes(phrase)
      );

      if (isAppointmentRequest) {
        console.log('🎯 Fallback appointment form triggered for:', messageText);
        setTimeout(() => {
          setFormData(prev => ({
            ...prev,
            name: contactData.name,
            email: contactData.email,
            phone: contactData.phone
          }));
          setShowAppointmentForm(true);
        }, 500);
      }
    } finally {
      setIsLoading(false);
    }
  };



  // Fallback response generator
  const getFallbackResponse = (message) => {
    const msg = message.toLowerCase().trim();

    // PRIORITY 1: APPOINTMENT BOOKING DETECTION - ENHANCED
    if (msg.includes('sure') || msg.includes('yes') || msg.includes('yeah') || msg.includes('yep') ||
        msg.includes('okay') || msg.includes('ok') || msg.includes('alright') || msg.includes('absolutely') ||
        msg.includes('schedule') || msg.includes('book') || msg.includes('appointment') ||
        msg.includes('consultation') || msg.includes('meeting') || msg.includes('call') ||
        msg.includes('discuss') || msg.includes('would you like to schedule') ||
        msg.includes('shall we schedule') || msg.includes('want to schedule') ||
        msg.includes('open appointment') || msg.includes('appointment form') || msg.includes('i\'m interested')) {

      // Trigger appointment form immediately
      console.log('🎯 Fallback appointment trigger activated for:', msg);
      setTimeout(() => {
        setFormData(prev => ({
          ...prev,
          name: contactData.name,
          email: contactData.email,
          phone: contactData.phone
        }));
        setShowAppointmentForm(true);
      }, 100);

      return `Perfect! I'll open the appointment booking form for you right now. Please fill in your details and preferred time, and we'll get back to you within 24 hours to confirm your consultation.`;
    }

    // PRIORITY 2: BUSINESS TYPE DETECTION (Enhanced)
    if (msg.includes('wood') || msg.includes('lumber') || msg.includes('timber') || msg.includes('carpentry') || msg.includes('furniture')) {
      return `Excellent! For your wood/carpentry business, Techrypt can help you showcase your craftsmanship and attract more customers through:

🌐 **Professional Website** - Display your portfolio and services
📱 **Social Media Marketing** - Show your work on Instagram/Facebook
🎨 **Branding Services** - Create a memorable brand identity
💳 **Online Ordering** - Accept custom orders online

Which service would help your wood business grow the most?`;
    } else if (msg.includes('restaurant') || msg.includes('food') || msg.includes('cafe') || msg.includes('dining')) {
      return `Great! For your restaurant business, Techrypt can help you grow with our comprehensive digital services. We specialize in helping food businesses attract more customers through professional websites, social media marketing, and online ordering systems. Which service would be most valuable for your restaurant?`;
    }

    // PRIORITY 3: SERVICE DETECTION
    if (msg === 'smm' || msg === 'social media marketing' || msg === 'social media' || msg === 'marketing' || msg === 'instagram' || msg === 'facebook' || msg === 'linkedin' || msg === '2') {
      return "Perfect! You've selected 📱 Social Media Marketing - Instagram, Facebook, LinkedIn growth. We help businesses grow their social media presence through targeted strategies and engaging content. Would you like to schedule a consultation to discuss your social media goals?";
    } else if (msg === 'website development' || msg === 'web development' || msg === 'website' || msg === 'web' || msg === 'site' || msg === 'seo' || msg === 'web dev' || msg === '1') {
      return "Excellent! You've selected 🌐 Website Development - Custom websites with SEO optimization. We create responsive, modern websites that help your business rank higher and attract more customers. Shall we schedule a consultation to discuss your website needs?";
    } else if (msg === 'branding services' || msg === 'branding' || msg === 'logo' || msg === 'brand' || msg === 'design' || msg === 'graphics' || msg === '3') {
      return "Great choice! You've selected 🎨 Branding Services - Logo design, brand identity, marketing materials. We create comprehensive brand identities that make your business stand out. Would you like to schedule a consultation to discuss your branding vision?";
    } else if (msg === 'chatbot development' || msg === 'chatbot' || msg === 'bot' || msg === 'ai' || msg === 'automation' || msg === 'llm' || msg === 'artificial intelligence' || msg === '4') {
      return "Awesome! You've selected 🤖 Chatbot Development - AI-powered customer service automation. We create intelligent chatbots that handle customer service 24/7. Shall we schedule a consultation to discuss your automation needs?";
    } else if (msg === 'automation packages' || msg === 'automation' || msg === 'process automation' || msg === 'business automation' || msg === '5') {
      return "Great selection! You've selected ⚡ Automation Packages - Business process automation solutions. We streamline your operations and save time with custom automation. Shall we schedule a consultation to discuss your automation needs?";
    } else if (msg === 'payment gateway integration' || msg === 'payment gateway' || msg === 'payment' || msg === 'gateway' || msg === 'stripe' || msg === 'paypal' || msg === 'payments' || msg === 'checkout' || msg === '6') {
      return "Perfect! You've selected 💳 Payment Gateway Integration - Stripe, PayPal, and custom solutions. We integrate secure payment systems to make transactions smooth for your customers. Would you like to schedule a consultation?";
    }

    // Handle business types with universal intelligence - enhanced patterns
    else if (msg.includes('business') || msg.includes('company') || msg.includes('store') || msg.includes('shop') ||
        msg.includes('i have') || msg.includes('i own') || msg.includes('i run') ||
        msg.includes('my ') || msg.includes('help me with my') || msg.includes('help with my') ||
        msg.includes('e-commerce') || msg.includes('ecommerce') || msg.includes('restaurant') ||
        msg.includes('salon') || msg.includes('gym') || msg.includes('clinic') || msg.includes('agency') ||
        msg.includes('firm') || msg.includes('practice') || msg.includes('service') ||
        msg.includes('how can you help') || msg.includes('what can you do for') ||
        (msg.includes('help me') && (msg.includes('business') || msg.includes('company') || msg.includes('store')))) {
      return getUniversalBusinessResponse(msg);
    }

    // Handle common queries
    else if (msg.includes('appointment') || msg.includes('schedule') || msg.includes('book') || msg.includes('meeting')) {
      return "I'd be happy to help you schedule an appointment! Let me open the booking form for you.";
    } else if (msg.includes('service') || msg.includes('what do you do') || msg.includes('what services') || msg.includes('list services') || msg === 'services' || msg.includes('what can you help') || msg.includes('what can techrypt do')) {
      return `Here are Techrypt's 6 core digital services:

1. 🌐 **Website Development** - Custom websites with SEO optimization
   • Responsive design for all devices
   • Search engine optimization (SEO)
   • Fast loading and secure hosting
   • Content management systems

2. 📱 **Social Media Marketing** - Instagram, Facebook, LinkedIn growth
   • Targeted advertising campaigns
   • Content creation and scheduling
   • Community management
   • Analytics and reporting

3. 🎨 **Branding Services** - Logo design, brand identity, marketing materials
   • Professional logo design
   • Brand identity packages
   • Marketing collateral design
   • Brand guidelines and strategy

4. 🤖 **Chatbot Development** - AI-powered customer service automation
   • 24/7 automated customer support
   • Lead generation and qualification
   • Appointment booking systems
   • Multi-platform integration

5. ⚡ **Automation Packages** - Business process automation solutions
   • Workflow automation
   • Email marketing automation
   • CRM integration
   • Custom business solutions

6. 💳 **Payment Gateway Integration** - Stripe, PayPal, and custom solutions
   • Secure payment processing
   • Multiple payment methods
   • Subscription management
   • E-commerce integration

Which service would you like to know more about? You can ask about specific features or book a consultation to discuss your needs!`;
    } else if (msg.includes('how long') || msg.includes('duration') || msg.includes('time') && (msg.includes('call') || msg.includes('appointment') || msg.includes('consultation'))) {
      return "Our consultation calls typically last 15-20 minutes. This gives us enough time to understand your business needs, discuss our services, and create a customized plan for your project. Would you like to schedule a consultation?";
    } else if (msg.includes('price') || msg.includes('cost') || msg.includes('pricing') || msg.includes('quote') || msg.includes('budget')) {
      return "Our pricing varies by project scope and requirements. I'd recommend scheduling a consultation to discuss your specific needs and get a custom quote tailored to your business.";
    } else if (msg.includes('location') || msg.includes('where') || msg.includes('address')) {
      return "We're based in Karachi, Pakistan, but we serve clients globally. Our team works remotely to provide 24/7 support worldwide. We can schedule virtual consultations at your convenience.";
    } else if (msg.includes('hello') || msg.includes('hi') || msg.includes('hey') || msg === 'hello' || msg === 'hi') {
      return "Hello! Welcome to Techrypt.io. I'm here to help you with our digital services and answer any questions you might have. How can I assist you today?";
    } else if (msg.includes('support') || msg.includes('hours') || msg.includes('available')) {
      return "Our support is available Monday through Friday, 9 AM to 6 PM EST. We also provide 24/7 emergency support for critical issues.";
    } else if (msg.includes('trial') || msg.includes('free') || msg.includes('demo')) {
      return "We don't offer a trial, but our initial consultation is completely free! During this consultation, we'll understand your needs and show you exactly how we can help your business grow.";
    } else if (msg.includes('portfolio') || msg.includes('work') || msg.includes('examples') || msg.includes('projects')) {
      return "We'd love to show you our portfolio! We have examples of websites, social media campaigns, branding projects, and automation solutions. Shall we schedule a consultation where we can showcase our work relevant to your industry?";
    } else if (msg.includes('tell me about') || msg.includes('about') || msg.includes('what is') || msg.includes('explain')) {
      return `Thank you for your question! I'm here to help you with Techrypt.io's digital services:

1. 🌐 Website Development with SEO optimization
2. 📱 Social Media Marketing to reach your target audience
3. 🎨 Branding Services for professional identity
4. 🤖 Chatbot Development for customer service
5. ⚡ Automation Packages to streamline operations
6. 💳 Payment Gateway Integration for seamless transactions

Could you tell me more about what you're looking for, or would you like to schedule a consultation to discuss your needs?`;
    }

    // Default intelligent response
    else {
      return `Thank you for your message! I'm here to help you with Techrypt.io's digital services:

• 🌐 Website Development
• 📱 Social Media Marketing
• 🎨 Branding Services
• 🤖 Chatbot Development
• ⚡ Automation Packages
• 💳 Payment Gateway Integration

Could you tell me more about what you're looking for, or would you like to schedule a consultation to discuss your needs?`;
    }
  };

  const getUniversalBusinessResponse = (message) => {
    // Extract business type from user's message
    let userBusinessType = extractBusinessType(message);

    // Check if it's an illegal business
    if (isIllegalBusiness(userBusinessType)) {
      return "I'm sorry, but I cannot assist with illegal activities or businesses. Techrypt.io only provides digital services for legitimate, legal businesses. Please let me know if you have a legal business I can help you with.";
    }

    // Correct spelling mistakes
    userBusinessType = correctSpelling(userBusinessType);

    // Simple, clean response without asterisks
    return `Great! For your ${userBusinessType}, we can help with:

1. Website Development
2. Social Media Marketing
3. Branding Services
4. Chatbot Development
5. Automation Packages
6. Payment Gateway Integration

Would you like to schedule a consultation or learn more about any specific service?`;
  };

  // Extract business type from user message
  const extractBusinessType = (message) => {
    const msg = message.toLowerCase();

    // Enhanced business patterns with better extraction for complete business names
    const patterns = [
      // "I have/own/run a [type] business" - captures complete business type
      /i have (?:a|an) (.+?)(?:\s+business|\s+company|\s+store|\s+shop)/,
      /i own (?:a|an) (.+?)(?:\s+business|\s+company|\s+store|\s+shop)/,
      /i run (?:a|an) (.+?)(?:\s+business|\s+company|\s+store|\s+shop)/,

      // "My [type] business" patterns
      /my (.+?)(?:\s+business|\s+company|\s+store|\s+shop)/,
      /help me with my (.+?)(?:\s+business|\s+company|\s+store|\s+shop)/,
      /help with my (.+?)(?:\s+business|\s+company|\s+store|\s+shop)/,

      // "[type] business" patterns
      /(.+?)(?:\s+business|\s+company|\s+store|\s+shop)/,

      // Single word business types that should get "business" added
      /\b(wood|furniture|construction|carpentry|lumber|timber|bakery|restaurant|cafe|salon|gym|hotel)\b/
    ];

    for (const pattern of patterns) {
      const match = msg.match(pattern);
      if (match && match[1]) {
        let businessType = match[1].trim();

        // Remove common words but keep compound business names
        businessType = businessType.replace(/\b(small|big|large|local|online|digital|new|old|the|can|you|help|me|with)\b/g, '').trim();

        // Skip if it's too short or contains question words
        if (!businessType || businessType.length < 3 ||
            ['how', 'what', 'when', 'where', 'why', 'who'].includes(businessType)) {
          continue;
        }

        // Always add "business" if not already present
        if (businessType && businessType.length > 2) {
          const businessWords = ['business', 'company', 'shop', 'store', 'service', 'clinic', 'agency', 'firm', 'center', 'salon', 'pool'];
          const hasBusinessWord = businessWords.some(word => businessType.includes(word));

          if (!hasBusinessWord) {
            businessType = businessType + ' business';
          }

          return businessType;
        }
      }
    }

    // Enhanced fallback with compound business types
    const businessKeywords = [
      'e-commerce store', 'ecommerce store', 'e-commerce business', 'ecommerce business',
      'coffee shop', 'swimming pool', 'fitness center', 'beauty salon', 'nail salon', 'hair salon',
      'real estate', 'law firm', 'accounting firm', 'consulting firm', 'space agency',
      'wood business', 'furniture business', 'construction business', 'carpentry business',
      'bakery', 'restaurant', 'cafe', 'shop', 'store', 'clinic', 'salon', 'gym', 'hotel',
      'agency', 'firm', 'company', 'service', 'practice', 'pool', 'fitness', 'spa', 'ecommerce', 'e-commerce'
    ];

    // Sort by length (longest first) to match compound terms first
    businessKeywords.sort((a, b) => b.length - a.length);

    for (const keyword of businessKeywords) {
      if (msg.includes(keyword)) {
        // Handle e-commerce variations
        if (keyword === 'ecommerce' || keyword === 'e-commerce') {
          return 'e-commerce store';
        }
        return keyword;
      }
    }

    return 'business';
  };

  // Check for illegal businesses
  const isIllegalBusiness = (businessType) => {
    const illegalKeywords = [
      'drug', 'drugs', 'cocaine', 'heroin', 'marijuana', 'cannabis', 'weed', 'meth',
      'kidnapping', 'kidnap', 'ransom', 'extortion', 'blackmail',
      'weapon', 'weapons', 'gun', 'guns', 'firearm', 'ammunition',
      'prostitution', 'escort', 'brothel', 'trafficking',
      'gambling', 'casino', 'betting', 'lottery',
      'fraud', 'scam', 'ponzi', 'pyramid',
      'counterfeit', 'fake', 'forgery',
      'hacking', 'cyber attack', 'malware'
    ];

    return illegalKeywords.some(keyword => businessType.toLowerCase().includes(keyword));
  };

  // Correct common spelling mistakes
  const correctSpelling = (businessType) => {
    const corrections = {
      'bakry': 'bakery',
      'bekery': 'bakery',
      'resturant': 'restaurant',
      'restraunt': 'restaurant',
      'saloon': 'salon',
      'jewalry': 'jewelry',
      'jewelery': 'jewelry',
      'pharamcy': 'pharmacy',
      'pharmcy': 'pharmacy',
      'consultancy': 'consulting',
      'consultng': 'consulting',
      'realestate': 'real estate',
      'realstate': 'real estate',
      'swiming': 'swimming',
      'swiming pool': 'swimming pool',
      'cofee': 'coffee',
      'cofee shop': 'coffee shop',
      'coffe': 'coffee',
      'coffe shop': 'coffee shop'
    };

    return corrections[businessType.toLowerCase()] || businessType;
  };

  // Generate intelligent solutions for any business type
  const getIntelligentSolutions = () => {
    // Universal response - all businesses get all 6 core services
    return `1. Website Development with SEO optimization
2. Social Media Marketing to reach your target audience
3. Branding Services for professional identity
4. Chatbot Development for customer service
5. Automation Packages to streamline operations
6. Payment Gateway Integration for seamless transactions`;
  };



  const stopListening = () => {
    setIsListening(false);
  };

  // Clear chat history
  const clearChatHistory = () => {
    const confirmClear = window.confirm('Are you sure you want to clear the chat history? This action cannot be undone.');
    if (confirmClear) {
      const defaultMessages = [
        {
          id: 1,
          text: "Hello! Welcome to Techrypt.io. I'm your AI assistant. I can help you with our services and schedule appointments. How can I assist you today?",
          sender: 'bot',
          timestamp: new Date()
        }
      ];
      setMessages(defaultMessages);
      localStorage.removeItem('techrypt-chat-messages');
    }
  };

  // Clear contact data for testing
  const clearContactData = () => {
    const confirmClear = window.confirm('Clear contact data? This will make the contact form appear again.');
    if (confirmClear) {
      setContactData({ name: '', email: '', phone: '' });
      localStorage.removeItem('techrypt-contact-data');
      setShowContactForm(true);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };



  // Form validation
  const validateContactForm = () => {
    const errors = {};

    if (!contactFormData.name.trim()) {
      errors.name = 'Name is required';
    }

    if (!contactFormData.email.trim()) {
      errors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contactFormData.email)) {
      errors.email = 'Email is not valid';
    }

    if (contactFormData.phone && !/^\d{10,15}$/.test(contactFormData.phone.replace(/\D/g, ''))) {
      errors.phone = 'Phone number must be 10-15 digits';
    }

    return errors;
  };

  const validateAppointmentForm = () => {
    const errors = {};

    if (!formData.name.trim()) {
      errors.name = 'Name is required';
    }

    if (!formData.email.trim()) {
      errors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errors.email = 'Email is not valid';
    }

    if (formData.phone && !/^\d{10,15}$/.test(formData.phone.replace(/\D/g, ''))) {
      errors.phone = 'Phone number must be 10-15 digits';
    }

    if (!formData.services || formData.services.length === 0) {
      errors.services = 'Please select at least one service';
    }

    if (!formData.date) {
      errors.date = 'Please select a date';
    }

    if (!formData.time) {
      errors.time = 'Please select a time';
    }

    return errors;
  };

  // Handle contact form submission
  const handleContactSubmit = () => {
    const errors = validateContactForm();
    setContactErrors(errors);

    if (Object.keys(errors).length > 0) {
      const errorMessages = Object.values(errors);
      setError(errorMessages[0]); // Show first error
      return;
    }

    // Save the form data to the main contact data
    setContactData(contactFormData);

    const botMessage = {
      id: Date.now() + 1,
      text: `Thank you, ${contactFormData.name}! How can I assist you today?`,
      sender: 'bot',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, botMessage]);
    setShowContactForm(false);
    setContactErrors({});
    setError(null);
    // Reset the contact form for next time
    setContactFormData({ name: '', email: '', phone: '' });
  };

  // Handle appointment form submission
  const handleAppointmentSubmit = () => {
    const errors = validateAppointmentForm();
    setAppointmentErrors(errors);

    if (Object.keys(errors).length > 0) {
      const errorMessages = Object.values(errors);
      setError(errorMessages[0]); // Show first error
      return;
    }

    // Close the appointment form first
    setShowAppointmentForm(false);

    // Show the thank you modal
    setShowThankYouModal(true);
    console.log("Thank you modal triggered:", showThankYouModal);
  
    

    const confirmationMessage = {
      id: Date.now() + 1,
      text: `🎉 Appointment Request Submitted!

Your appointment request has been received:

Details:
• Services: ${formData.services.join(', ')}
• Date: ${formData.date}
• Time: ${formData.time}
• Contact: ${formData.email}

📧 Next Steps:
• Our team will contact you within 24 hours to confirm
• You'll receive a confirmation email shortly
• We'll send calendar details once confirmed

Thank you for choosing Techrypt.io! 🚀`,
      sender: 'bot',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, confirmationMessage]);
    setFormData({ name: '', email: '', phone: '', services: [], date: '', time: '', notes: '' });
    setAppointmentErrors({});
    setError(null);
  };

  if (!isOpen) return null;

  return (
    <div className={`techrypt-chatbot-overlay ${isMinimized ? 'minimized' : ''}`}>
      <div className={`techrypt-chatbot-container ${isMinimized ? 'minimized' : ''}`}>
        {/* Mobile Header - Only visible on screens ≤768px */}
        <div
          className="techrypt-chatbot-header techrypt-chatbot-header-mobile md:hidden"
          onClick={isMinimized ? () => setIsMinimized(false) : undefined}
          style={isMinimized ? { cursor: 'pointer' } : {}}
        >
          <div className="techrypt-chatbot-header-content">
            <div className="techrypt-chatbot-avatar">
              <BsRobot />
            </div>
            <div className="techrypt-chatbot-title">
              <h3>Techrypt AI</h3>
            </div>
          </div>
          <div className="techrypt-chatbot-header-actions">
            {!isMinimized && (
              <>
                <button
                  className="techrypt-chatbot-appointment"
                  onClick={() => {
                    setFormData(prev => ({
                      ...prev,
                      name: contactData.name || '',
                      email: contactData.email || '',
                      phone: contactData.phone || ''
                    }));
                    setShowAppointmentForm(true);
                  }}
                  title="Book an Appointment"
                >
                  <img src={calenderIcon} alt="Appointment" className="header-icon" />
                </button>
                <button
                  className="techrypt-chatbot-clear"
                  onClick={clearChatHistory}
                  title="Clear Chat History"
                >
                  <img src={binIcon} alt="Clear Chat" className="header-icon" />
                </button>
              </>
            )}
            <button
              className="techrypt-chatbot-minimize"
              onClick={(e) => {
                e.stopPropagation();
                setIsMinimized(!isMinimized);
              }}
              title={isMinimized ? "Expand" : "Minimize"}
            >
              <img
                src={isMinimized ? calenderIcon : minimizeIcon}
                alt={isMinimized ? "Expand" : "Minimize"}
                className="header-icon"
              />
            </button>
            <button
              className="techrypt-chatbot-close"
              onClick={onClose}
              title="Close Chatbot"
            >
              <img src={closeIcon} alt="Close Chatbot" className="header-icon" />
            </button>
          </div>
        </div>

        {/* Desktop Header - Only visible on screens >768px */}
        <div
          className="techrypt-chatbot-header techrypt-chatbot-header-desktop hidden md:flex"
          onClick={isMinimized ? () => setIsMinimized(false) : undefined}
          style={isMinimized ? { cursor: 'pointer' } : {}}
        >
          <div className="techrypt-chatbot-header-content">
            <div className="techrypt-chatbot-avatar">
              <BsRobot />
            </div>
            <div className="techrypt-chatbot-title">
              <h3>Techrypt AI</h3>
            </div>
          </div>
          <div className="techrypt-chatbot-header-actions">
            {!isMinimized && (
              <>
                <button
                  className="techrypt-chatbot-appointment"
                  onClick={() => {
                    setFormData(prev => ({
                      ...prev,
                      name: contactData.name || '',
                      email: contactData.email || '',
                      phone: contactData.phone || ''
                    }));
                    setShowAppointmentForm(true);
                  }}
                  title="Book an Appointment"
                >
                  <img src={calenderIcon} alt="Appointment" className="header-icon" />
                </button>
                <button
                  className="techrypt-chatbot-clear"
                  onClick={clearChatHistory}
                  title="Clear Chat History"
                >
                  <img src={binIcon} alt="Clear Chat" className="header-icon" />
                </button>
              </>
            )}
            <button
              className="techrypt-chatbot-minimize"
              onClick={(e) => {
                e.stopPropagation();
                setIsMinimized(!isMinimized);
              }}
              title={isMinimized ? "Expand" : "Minimize"}
            >
              <img
                src={isMinimized ? calenderIcon : minimizeIcon}
                alt={isMinimized ? "Expand" : "Minimize"}
                className="header-icon"
              />
            </button>
            <button
              className="techrypt-chatbot-close"
              onClick={onClose}
              title="Close Chatbot"
            >
              <img src={closeIcon} alt="Close Chatbot" className="header-icon" />
            </button>
          </div>
        </div>



        {/* Error Alert */}
        {error && !isMinimized && (
          <div className="techrypt-chatbot-error">
            <span>{error}</span>
            <button onClick={() => setError(null)}>×</button>
          </div>
        )}

        {/* Messages */}
        {!isMinimized && (
        <div className="techrypt-chatbot-messages">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`techrypt-message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
            >
              <div className="techrypt-message-avatar">
                {message.sender === 'user' ? <BsPerson /> : <BsRobot />}
              </div>
              <div className="techrypt-message-content">
                <div className="techrypt-message-bubble">
                  <p>{message.text}</p>
                  {message.sender === 'bot' && (
                    <button
                      className="techrypt-speak-button"
                      onClick={() => speakText(message.text)}
                      title="Read Aloud"
                    >
                      <BsVolumeUp />
                    </button>
                  )}
                </div>
                <span className="techrypt-message-time">
                  {message.timestamp.toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </span>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="techrypt-message bot-message">
              <div className="techrypt-message-avatar">
                {/* Apply green background and black icon */}
                <div className="avatar-icon">
                  <BsRobot />
                </div>
              </div>
              <div className="techrypt-message-content">
                <div className="techrypt-typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>

          )}
          <div ref={messagesEndRef} />
        </div>
        )}

        {/* Input */}
        {!isMinimized && (
        <div className="techrypt-chatbot-input">
          <div className="techrypt-input-container">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Inquire here..."
              disabled={isLoading}
              rows="1"
            />
            
            <button
              className="techrypt-send-button"
              onClick={() => sendMessage()}
              disabled={isLoading || !inputMessage.trim()}
              title="Send Message"
            >
              <BsSend />
            </button>
          </div>
        </div>
        )}

        {/* Contact Form Modal */}
        {showContactForm && (
          <div className="techrypt-form-overlay">
            <div className="techrypt-form-modal">
              <div className="techrypt-form-header">
                <h3>👋 Let's Get to Know You!</h3>
                <button onClick={() => setShowContactForm(false)}>×</button>
              </div>
              <div className="techrypt-form-content">
                <p>Please share your contact information so I can provide you with personalized assistance.</p>
                <div className="techrypt-form-fields">
                  <div className="techrypt-form-field">
                    <label>Full Name *</label>
                    <input
                      type="text"
                      value={contactFormData.name}
                      onChange={(e) => {
                        setContactFormData(prev => ({ ...prev, name: e.target.value }));
                        if (contactErrors.name) {
                          setContactErrors(prev => ({ ...prev, name: '' }));
                        }
                      }}
                      placeholder="Enter your full name"
                      className={contactErrors.name ? 'error' : ''}
                      required
                    />
                    {contactErrors.name && <span className="techrypt-field-error">{contactErrors.name}</span>}
                  </div>
                  <div className="techrypt-form-field">
                    <label>Email Address *</label>
                    <input
                      type="email"
                      value={contactFormData.email}
                      onChange={(e) => {
                        setContactFormData(prev => ({ ...prev, email: e.target.value }));
                        if (contactErrors.email) {
                          setContactErrors(prev => ({ ...prev, email: '' }));
                        }
                      }}
                      placeholder="Enter your email address"
                      className={contactErrors.email ? 'error' : ''}
                      required
                    />
                    {contactErrors.email && <span className="techrypt-field-error">{contactErrors.email}</span>}
                  </div>
                  <div className="techrypt-form-field">
                    <label>Phone Number (Optional)</label>
                    <input
                      type="tel"
                      value={contactFormData.phone}
                      onChange={(e) => {
                        const value = e.target.value.replace(/[^0-9+\-() ]/g, '');
                        setContactFormData(prev => ({ ...prev, phone: value }));
                        if (contactErrors.phone) {
                          setContactErrors(prev => ({ ...prev, phone: '' }));
                        }
                      }}
                      placeholder="e.g., 1234567890 or +1-234-567-8900"
                      className={contactErrors.phone ? 'error' : ''}
                    />
                    {contactErrors.phone && <span className="techrypt-field-error">{contactErrors.phone}</span>}
                  </div>
                </div>
                <div className="techrypt-form-actions">
                  <button
                    className="techrypt-form-cancel"
                    onClick={() => setShowContactForm(false)}
                  >
                    Cancel
                  </button>
                  <button
                    className="techrypt-form-submit"
                    onClick={handleContactSubmit}
                    disabled={isLoading || !contactFormData.name || !contactFormData.email}
                  >
                    {isLoading ? 'Submitting...' : 'Save & Continue'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Appointment Form Modal */}
        {showAppointmentForm && (
          <div className="techrypt-form-overlay">
            <div className="techrypt-form-modal techrypt-appointment-modal">
              <div className="techrypt-form-header">
                <h3>📅 Schedule Your Appointment</h3>
                <button onClick={() => setShowAppointmentForm(false)}>×</button>
              </div>
              <div className="techrypt-form-content">
                <p>Complete your appointment details below. Your contact information has been pre-filled.</p>
                <div className="techrypt-form-fields">
                  <div className="techrypt-form-row">
                    <div className="techrypt-form-field">
                      <label>Full Name *</label>
                      <input
                        type="text"
                        value={formData.name}
                        onChange={(e) => {
                          setFormData(prev => ({ ...prev, name: e.target.value }));
                          if (appointmentErrors.name) {
                            setAppointmentErrors(prev => ({ ...prev, name: '' }));
                          }
                        }}
                        className={appointmentErrors.name ? 'error' : ''}
                        required
                      />
                      {appointmentErrors.name && <span className="techrypt-field-error">{appointmentErrors.name}</span>}
                    </div>
                    <div className="techrypt-form-field">
                      <label>Email Address *</label>
                      <input
                        type="email"
                        value={formData.email}
                        onChange={(e) => {
                          setFormData(prev => ({ ...prev, email: e.target.value }));
                          if (appointmentErrors.email) {
                            setAppointmentErrors(prev => ({ ...prev, email: '' }));
                          }
                        }}
                        className={appointmentErrors.email ? 'error' : ''}
                        required
                      />
                      {appointmentErrors.email && <span className="techrypt-field-error">{appointmentErrors.email}</span>}
                    </div>
                  </div>
                  <div className="techrypt-form-field">
                    <label>Phone Number</label>
                    <input
                      type="tel"
                      value={formData.phone}
                      onChange={(e) => {
                        const value = e.target.value.replace(/[^0-9+\-() ]/g, '');
                        setFormData(prev => ({ ...prev, phone: value }));
                        if (appointmentErrors.phone) {
                          setAppointmentErrors(prev => ({ ...prev, phone: '' }));
                        }
                      }}
                      placeholder="e.g., 1234567890 or +1-234-567-8900"
                      className={appointmentErrors.phone ? 'error' : ''}
                    />
                    {appointmentErrors.phone && <span className="techrypt-field-error">{appointmentErrors.phone}</span>}
                  </div>
                  <div className="techrypt-form-field">
                    <label>Services * (Select all that apply)</label>
                    <div className="techrypt-services-grid">
                      {[
                        { id: 'website', name: 'Website Development', icon: '🌐', desc: 'Custom websites with SEO optimization' },
                        { id: 'social', name: 'Social Media Marketing', icon: '📱', desc: 'Instagram, Facebook, LinkedIn growth' },
                        { id: 'branding', name: 'Branding Services', icon: '🎨', desc: 'Logo design, brand identity, marketing materials' },
                        { id: 'chatbot', name: 'Chatbot Development', icon: '🤖', desc: 'AI-powered customer service automation' },
                        { id: 'automation', name: 'Automation Packages', icon: '⚡', desc: 'Business process automation solutions' },
                        { id: 'payment', name: 'Payment Gateway Integration', icon: '💳', desc: 'Stripe, PayPal, and custom solutions' }
                      ].map(service => (
                        <div key={service.id} className="techrypt-service-checkbox">
                          <label>
                            <input
                              type="checkbox"
                              checked={formData.services.includes(service.name)}
                              onChange={(e) => {
                                const isChecked = e.target.checked;
                                setFormData(prev => ({
                                  ...prev,
                                  services: isChecked
                                    ? [...prev.services, service.name]
                                    : prev.services.filter(s => s !== service.name)
                                }));
                                if (appointmentErrors.services) {
                                  setAppointmentErrors(prev => ({ ...prev, services: '' }));
                                }
                              }}
                            />
                            <span className="techrypt-service-content">
                              <span className="techrypt-service-icon">{service.icon}</span>
                              <span className="techrypt-service-name">{service.name}</span>
                              <span className="techrypt-service-desc">{service.desc}</span>
                            </span>
                          </label>
                        </div>
                      ))}
                    </div>
                    {appointmentErrors.services && <span className="techrypt-field-error">{appointmentErrors.services}</span>}
                  </div>
                  <div className="techrypt-form-row">
                    <div className="techrypt-form-field">
                      <label>Preferred Date *</label>
                      <input
                        type="date"
                        value={formData.date}
                        onChange={(e) => {
                          setFormData(prev => ({ ...prev, date: e.target.value }));
                          if (appointmentErrors.date) {
                            setAppointmentErrors(prev => ({ ...prev, date: '' }));
                          }
                        }}
                        min={new Date(Date.now() + 86400000).toISOString().split('T')[0]}
                        className={appointmentErrors.date ? 'error' : ''}
                        required
                      />
                      {appointmentErrors.date && <span className="techrypt-field-error">{appointmentErrors.date}</span>}
                    </div>
                    <div className="techrypt-form-field">
                      <label>Preferred Time *</label>
                      <input
                        type="time"
                        value={formData.time}
                        onChange={(e) => {
                          setFormData(prev => ({ ...prev, time: e.target.value }));
                          if (appointmentErrors.time) {
                            setAppointmentErrors(prev => ({ ...prev, time: '' }));
                          }
                        }}
                        className={appointmentErrors.time ? 'error' : ''}
                        required
                      />
                      {appointmentErrors.time && <span className="techrypt-field-error">{appointmentErrors.time}</span>}
                    </div>
                  </div>
                  <div className="techrypt-form-field">
                    <label>Additional Notes (Optional)</label>
                    <textarea
                      value={formData.notes}
                      onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
                      placeholder="Any specific requirements or questions..."
                      rows="3"
                    />
                  </div>
                </div>
                <div className="techrypt-business-hours">
                  <strong>Business Hours:</strong><br />
                  Monday - Friday: 9:00 AM - 6:00 PM EST<br />
                  Saturday: 10:00 AM - 4:00 PM EST<br />
                  Sunday: Closed
                </div>
                <div className="techrypt-form-actions">
                  <button
                    className="techrypt-form-cancel"
                    onClick={() => setShowAppointmentForm(false)}
                  >
                    Cancel
                  </button>
                  <button
                    className="techrypt-form-submit"
                    onClick={handleAppointmentSubmit}
                    disabled={!formData.name || !formData.email || !formData.services.length || !formData.date || !formData.time}
                  >
                    Book Appointment
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Thank You Modal */}
        {showThankYouModal && (
          <div className="techrypt-form-overlay" style={{zIndex: 1000}}>
            <div className="techrypt-form-modal" style={{ maxWidth: '400px' }}>
              <div className="techrypt-form-header">
                <h3 style={{ color: 'black' }}>🎉 Appointment Booked!</h3>
                <button onClick={() => setShowThankYouModal(false)}>×</button>
              </div>
              <div className="techrypt-form-content">
                <div className="flex flex-col items-center text-center mb-4">
                  <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mb-4">
                    <div className="w-10 h-10 text-primary text-3xl">✓</div>
                  </div>
                  <h4 className="text-xl font-bold text-white mb-2">Thank You!</h4>
                  <p className="text-gray-300 mb-4">
                    Your appointment request has been successfully submitted.
                  </p>
                </div>
                
                <div className="bg-black/30 p-4 rounded-lg mb-4">
                  <h5 className="text-primary font-bold mb-2">Next Steps:</h5>
                  <ul className="text-gray-300 text-sm space-y-2">
                    <li className="flex items-start">
                      <span className="text-primary mr-2">•</span>
                      Our team will contact you within 24 hours
                    </li>
                    <li className="flex items-start">
                      <span className="text-primary mr-2">•</span>
                      You'll receive a confirmation email shortly
                    </li>
                    <li className="flex items-start">
                      <span className="text-primary mr-2">•</span>
                      We'll send calendar details once confirmed
                    </li>
                  </ul>
                </div>
                
                <div className="techrypt-form-actions">
                  <button
                    className="techrypt-form-submit w-full"
                    onClick={() => setShowThankYouModal(false)}
                  >
                    Close
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TechryptChatbot;
