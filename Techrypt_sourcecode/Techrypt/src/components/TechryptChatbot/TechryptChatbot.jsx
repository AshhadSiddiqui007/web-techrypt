import React, { useState, useEffect, useRef } from 'react';
import './TechryptChatbot.css';
import { BsRobot, BsPerson, BsSend, BsVolumeUp, BsX } from 'react-icons/bs';
import calenderIcon from "/Images/chatbot/calender.svg";
import minimizeIcon from "/Images/chatbot/minimize.svg";
import binIcon from "/Images/chatbot/bin.svg";
import closeIcon from "/Images/chatbot/close.svg";
// Service icons imports
import brandingIcon from "/Images/appointmentform/branding.svg";
import digitalMarketingIcon from "/Images/appointmentform/digital-marketing.svg";
import webdevelopmentIcon from "/Images/appointmentform/webdevelopment.svg";
import chatbotIcon from "/Images/appointmentform/chatbot.svg";
import influencerMarketingIcon from "/Images/appointmentform/influencer-marketing.svg";
import videoProductionIcon from "/Images/appointmentform/video-production.svg";
import customSoftwareIcon from "/Images/appointmentform/custom-software.svg";
import mobileAppIcon from "/Images/appointmentform/mobile-app.svg";
import cloudSolutionsIcon from "/Images/appointmentform/cloud-solutions.svg";

// Service icon mapping
const serviceIcons = {
  'branding': brandingIcon,
  'digital-marketing': digitalMarketingIcon,
  'web-development': webdevelopmentIcon,
  'ai-chatbots': chatbotIcon,
  'influencer-marketing': influencerMarketingIcon,
  'video-production': videoProductionIcon,
  'custom-software': customSoftwareIcon,
  'mobile-app': mobileAppIcon,
  'cloud-solutions': cloudSolutionsIcon
};

const TechryptChatbot = ({ isOpen, onClose, openAppointmentDirect }) => {
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
  // Track bot responses for landing page limit
  const [botResponseCount, setBotResponseCount] = useState(1); // initial bot message
  const [chatDisabled, setChatDisabled] = useState(false);
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
  // MODIFICATION: Removed conflict-related state variables since multiple appointments per time slot are now allowed
  // const [conflictData, setConflictData] = useState(null);
  // const [showConflictModal, setShowConflictModal] = useState(false);
  const [contactErrors, setContactErrors] = useState({});
  const [appointmentErrors, setAppointmentErrors] = useState({});

  // Add new state variable for the thank you modal
  const [showThankYouModal, setShowThankYouModal] = useState(false);

  // Add this with your other state variables
  const [showLoadingOverlay, setShowLoadingOverlay] = useState(false);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Show contact form automatically after welcome message on first open
  useEffect(() => {
  const alreadySubmitted = localStorage.getItem("contactFormSubmitted") === "true";
  if (!alreadySubmitted) {
    setShowContactForm(true); // Only show if not already submitted
  }
}, []);

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
    if (!messageText.trim() || chatDisabled) return;

    const userMessage = {
      id: Date.now(),
      text: messageText,
      sender: 'user',
      timestamp: new Date()
    };

    console.debug('[Chatbot] User message appended:', userMessage);
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setError(null); // Clear any previous errors

    try {
      // Try to connect to Smart AI backend with enhanced context
      const response = await fetch(`${import.meta.env.VITE_FLASK_BACKEND}/chat`, {
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

      // Only use fallback if backend response is missing or empty string/null/undefined
      let botText = (typeof data.response === 'string' && data.response.trim() !== '') ? data.response : getFallbackResponse(messageText);

      const botMessage = {
        id: Date.now() + 1,
        text: botText,
        sender: 'bot',
        timestamp: new Date(),
        showContactForm: data.show_contact_form,
        showAppointmentForm: data.show_appointment_form
      };

      console.debug('[Chatbot] Bot message appended:', botMessage);
      setMessages(prev => [...prev, botMessage]);
      // If landing page limit is enabled, count bot responses
      if (props && props.limitBotResponses) {
        setBotResponseCount(prev => {
          const newCount = prev + 1;
          if (newCount >= 4) {
            setChatDisabled(true);
            setShowContactForm(false);
            // Prefill appointment form with contactData and open main appointment form
            setFormData(prev => ({
              ...prev,
              name: contactData.name || '',
              email: contactData.email || '',
              phone: contactData.phone || ''
            }));
            setShowAppointmentForm(true); // This triggers the main appointment form modal
          }
          return newCount;
        });
      }

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

      // Use fallback response ONLY if no bot message was already added
      const botMessage = {
        id: Date.now() + 1,
        text: getFallbackResponse(messageText),
        sender: 'bot',
        timestamp: new Date()
      };

      console.debug('[Chatbot] Bot fallback message appended:', botMessage);
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
      return "We don't offer a trial, but our initial consultation is completely free! During this consultation, we'll understand your needs and show you exactly how we can help.";
    } else if (msg.includes('portfolio') || msg.includes('work') || msg.includes('examples') || msg.includes('projects')) {
      return "We'd love to show you our portfolio! We have examples of websites, social media campaigns, branding projects, and automation solutions. Shall we schedule a consultation where we can showcase our work relevant to your industry?";
    } else if (msg.includes('tell me about') || msg.includes('about') || msg.includes('what is') || msg.includes('explain')) {
      return `Thank you for your question! I'm here to help you with Techrypt.io's digital services:

1.  Website Development with SEO optimization
2.  Social Media Marketing to reach your target audience
3.  Branding Services for professional identity
4.  Chatbot Development for customer service
5.  Automation Packages to streamline operations
6.  Payment Gateway Integration for seamless transactions

Could you tell me more about what you're looking for, or would you like to schedule a consultation to discuss your needs?`;
    }

    // Default intelligent response
    else {
      return `Thank you for your message! I'm here to help you with Techrypt.io's digital services:

•  Website Development
•  Social Media Marketing
•  Branding Services
•  Chatbot Development
•  Automation Packages
•  Payment Gateway Integration

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
      'prostitution',
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

  // Generate available time slots based on business hours and selected date (timezone-aware)
  const getAvailableTimeSlots = () => {
    if (!formData.date) {
      console.log('🕒 No date selected, returning empty time slots');
      return [];
    }

    const selectedDate = new Date(formData.date);
    const dayOfWeek = selectedDate.getDay(); // 0=Sunday, 1=Monday, ..., 6=Saturday

    console.log('🕒 Generating time slots for:', {
      date: formData.date,
      dayOfWeek: dayOfWeek,
      dayName: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][dayOfWeek]
    });

    let timeSlots = [];

    if (dayOfWeek === 0) {
      // Sunday - Closed
      console.log('🕒 Sunday selected - no time slots available (closed)');
      return [];
    } else {
      // Get business hours in user's timezone
      const localBusinessHours = getLocalBusinessHours();
      console.log('🕒 Local business hours:', localBusinessHours);

      if (dayOfWeek >= 1 && dayOfWeek <= 5) {
        // Monday-Friday: Use converted weekday hours (9 AM - 6 PM PKT)
        console.log('🕒 Weekday selected - generating slots from', localBusinessHours.weekdays.start, 'to', localBusinessHours.weekdays.end);
        timeSlots = generateTimeSlots(localBusinessHours.weekdays.start, localBusinessHours.weekdays.end);
      } else if (dayOfWeek === 6) {
        // Saturday: Use converted Saturday hours (10 AM - 4 PM PKT)
        console.log('🕒 Saturday selected - generating slots from', localBusinessHours.saturday.start, 'to', localBusinessHours.saturday.end);
        timeSlots = generateTimeSlots(localBusinessHours.saturday.start, localBusinessHours.saturday.end);
      }
    }

    console.log('🕒 Generated time slots:', timeSlots);
    return timeSlots;
  };

    const generateTimeSlots = (startTime, endTime) => {
      console.log('🕒 Generating 3-hour range slots from', startTime, 'to', endTime);

      if (!startTime || !endTime) {
        console.warn('🕒 Invalid start or end time:', { startTime, endTime });
        return [];
      }

      const slots = [];

      try {
        const [startH, startM] = startTime.split(':').map(Number);
        const [endH, endM] = endTime.split(':').map(Number);

        let start = new Date(2000, 0, 1, startH, startM);
        let end = new Date(2000, 0, 1, endH, endM);

        // Handle overnight ranges (e.g. 6 PM to 3 AM)
        if (end <= start) {
          end.setDate(end.getDate() + 1);
        }

        // Generate up to 3 slots, each 3 hours long
        for (let i = 0; i < 3; i++) {
          const slotStart = new Date(start.getTime() + i * 3 * 60 * 60 * 1000); // +3h steps
          const slotEnd = new Date(slotStart.getTime() + 3 * 60 * 60 * 1000); // 3h duration

          if (slotStart >= end || slotEnd > end) break;

          const formatTime = (date) => {
            return date.toLocaleTimeString('en-US', {
              hour: '2-digit',
              minute: '2-digit',
              hour12: true,
            });
          };

          const slotRange = `${formatTime(slotStart)} - ${formatTime(slotEnd)}`;
          slots.push(slotRange);
        }

        console.log('🕒 Final readable time slots:', slots);
        return slots;
      } catch (error) {
        console.error('🕒 Error generating time slots:', error);
        return [];
      }
    };




  // Format time for display (convert 24-hour to 12-hour format)
  const formatTimeDisplay = (time24) => {
    const [hours, minutes] = time24.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const hour12 = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;
    return `${hour12}:${minutes} ${ampm}`;
  };

  // Format time slot for display (handles slot values like "6pm-9pm", "9pm-12am", "12am-3am")
  const formatTimeSlotDisplay = (timeSlot) => {
    if (!timeSlot) return 'Not specified';

    // Handle the predefined time slot values with consultation details
    const timeSlotMap = {
      '6pm-9pm': '6:00 PM - 9:00 PM PKT (15-20 min consultation - exact time to be confirmed within 24 hours)',
      '9pm-12am': '9:00 PM - 12:00 AM PKT (15-20 min consultation - exact time to be confirmed within 24 hours)',
      '12am-3am': '12:00 AM - 3:00 AM PKT (15-20 min consultation - exact time to be confirmed within 24 hours)'
    };

    // Return the formatted display if it's a known slot
    if (timeSlotMap[timeSlot]) {
      return timeSlotMap[timeSlot];
    }

    // Fallback: if it's a regular time format, use the original formatter
    if (timeSlot.includes(':')) {
      return formatTimeDisplay(timeSlot);
    }

    // Final fallback: return as-is
    return timeSlot;
  };

  // Check if selected date is Sunday
  const isSelectedDateSunday = () => {
    if (!formData.date) return false;
    const selectedDate = new Date(formData.date);
    return selectedDate.getDay() === 0; // 0 = Sunday
  };

  // Timezone utilities
  const PAKISTAN_TIMEZONE = 'Asia/Karachi';
  const getUserTimezone = () => {
    return Intl.DateTimeFormat().resolvedOptions().timeZone;
  };

  // Simplified timezone conversion using Intl API
  const convertPakistanTimeToLocal = (pakistanTime) => {
    const [hours, minutes] = pakistanTime.split(':').map(Number);

    // Create a date object representing the time in Pakistan
    const today = new Date();
    const pakistanDateTime = new Date();
    pakistanDateTime.setHours(hours, minutes, 0, 0);

    // Format the time in Pakistan timezone
    const pakistanTimeFormatted = pakistanDateTime.toLocaleString('en-US', {
      timeZone: PAKISTAN_TIMEZONE,
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    });

    // Create a new date with Pakistan time and convert to user's timezone
    const [pakHours, pakMinutes] = pakistanTimeFormatted.split(':').map(Number);
    const baseDate = new Date();
    baseDate.setHours(pakHours, pakMinutes, 0, 0);

    // Get the time in user's timezone
    const userTime = baseDate.toLocaleString('en-US', {
      timeZone: getUserTimezone(),
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    });

    return userTime;
  };

  // Convert local time back to Pakistan time for backend
  const convertLocalTimeToPakistan = (localTime) => {
    const [hours, minutes] = localTime.split(':').map(Number);

    // Create date in user's timezone
    const localDate = new Date();
    localDate.setHours(hours, minutes, 0, 0);

    // Convert to Pakistan timezone
    const pakistanTime = localDate.toLocaleString('en-US', {
      timeZone: PAKISTAN_TIMEZONE,
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    });

    return pakistanTime;
  };

  // Get business hours in user's timezone
  const getLocalBusinessHours = () => {
    const userTimezone = getUserTimezone();

    try {
      // REVERTED: Original Pakistan business hours (evening/overnight schedule)
      // Monday-Friday: 6:00 PM - 3:00 AM (next day) PKT
      // Saturday: 6:00 PM - 10:00 PM PKT
      const weekdayStart = convertPakistanTimeToLocal('18:00');
      const weekdayEnd = convertPakistanTimeToLocal('03:00');
      const saturdayStart = convertPakistanTimeToLocal('18:00');
      const saturdayEnd = convertPakistanTimeToLocal('22:00');

      return {
        weekdays: {
          start: weekdayStart,
          end: weekdayEnd,
          display: `${formatTimeDisplay(weekdayStart)} - ${formatTimeDisplay(weekdayEnd)}`
        },
        saturday: {
          start: saturdayStart,
          end: saturdayEnd,
          display: `${formatTimeDisplay(saturdayStart)} - ${formatTimeDisplay(saturdayEnd)}`
        },
        timezone: userTimezone,
        pakistanTimezone: PAKISTAN_TIMEZONE
      };
    } catch (error) {
      // Fallback to Pakistan time if conversion fails
      console.warn('Timezone conversion failed, using Pakistan time:', error);
      return {
        weekdays: {
          start: '18:00',
          end: '03:00',
          display: '6:00 PM - 3:00 AM (Pakistan Time)'
        },
        saturday: {
          start: '18:00',
          end: '22:00',
          display: '6:00 PM - 10:00 PM (Pakistan Time)'
        },
        timezone: PAKISTAN_TIMEZONE,
        pakistanTimezone: PAKISTAN_TIMEZONE
      };
    }
  };

  // Helper function to check if a time slot is in the past for today's date
  const isTimeSlotInPast = (timeSlot) => {
    if (!formData.date) return false;
    
    const selectedDate = new Date(formData.date);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    // Only check for past times if the selected date is today
    if (selectedDate.getTime() !== today.getTime()) {
      return false;
    }
    
    // Parse the time slot (e.g., "6pm-9pm" or "6:00 PM – 9:00 PM")
    let startTimeStr;
    if (timeSlot.includes('–')) {
      startTimeStr = timeSlot.split('–')[0].trim();
    } else if (timeSlot.includes('-')) {
      startTimeStr = timeSlot.split('-')[0].trim();
    } else {
      return false; // Invalid format
    }
    
    // Convert time string to 24-hour format
    let hour24;
    if (timeSlot.includes('6pm') || startTimeStr.includes('6:00 PM')) {
      hour24 = 18;
    } else if (timeSlot.includes('9pm') || startTimeStr.includes('9:00 PM')) {
      hour24 = 21;
    } else if (timeSlot.includes('12am') || startTimeStr.includes('12:00 AM')) {
      hour24 = 0;
    } else {
      return false; // Unknown time slot
    }
    
    // Create datetime for the time slot
    const slotDateTime = new Date();
    slotDateTime.setHours(hour24, 0, 0, 0);
    
    // Get current time
    const currentTime = new Date();
    
    // Check if the time slot has passed
    return slotDateTime < currentTime;
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
    } else {
      // Validate that selected date is not in the past
      const selectedDate = new Date(formData.date);
      const today = new Date();
      today.setHours(0, 0, 0, 0); // Reset time to start of day for comparison
      
      if (selectedDate < today) {
        errors.date = 'Please select a date that is today or in the future';
      }
    }

    if (!formData.time) {
      errors.time = 'Please select a time';
    } else if (formData.date) {
      // Validate that selected time is not in the past (if date is today)
      const selectedDate = new Date(formData.date);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      // Only check time if the selected date is today
      if (selectedDate.getTime() === today.getTime()) {
        if (isTimeSlotInPast(formData.time)) {
          errors.time = 'Please select a time slot that has not already passed';
        }
      }
    }

    return errors;
  };

  // Handle contact form submission
  const handleContactSubmit = async () => {
  if (!contactFormData.name || !contactFormData.email) return;

  setIsLoading(true);

  try {
    const res = await fetch(`${import.meta.env.VITE_NODE_BACKEND}/contact-info`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(contactFormData),
    });

    const result = await res.json();

    if (result.success) {
      localStorage.setItem("contactFormSubmitted", "true");
      setShowContactForm(false);
    } else {
      console.error("Error saving contact info:", result.error);
    }
  } catch (error) {
    console.error("Network error:", error);
  }

  setIsLoading(false);
};


  // Handle appointment form submission
  const handleAppointmentSubmit = async () => {
    const errors = validateAppointmentForm();
    setAppointmentErrors(errors);

    if (Object.keys(errors).length > 0) {
      const errorMessages = Object.values(errors);
      setError(errorMessages[0]); // Show first error
      return;
    }

    setIsLoading(true);
    setShowLoadingOverlay(true);
    setError(null);

    try {
      // Prepare appointment data for MongoDB - convert time to Pakistan timezone
      const pakistanTime = convertLocalTimeToPakistan(formData.time);

      const appointmentData = {
        name: formData.name.trim(),
        email: formData.email.trim(),
        phone: formData.phone.trim(),
        services: formData.services,
        preferred_date: formData.date,
        preferred_time: formData.time,
        user_timezone: getUserTimezone(),
        notes: formData.notes.trim(),
        status: 'Pending',
        created_at: new Date().toISOString(),
        source: 'chatbot_form'
      };

      console.log('📅 Submitting appointment data:', appointmentData);

      // --- Node.js backend API call ---
      const response = await fetch(`${import.meta.env.VITE_NODE_BACKEND}/appointments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(appointmentData)
      });

      const result = await response.json();
      console.log('📊 Backend response:', result);

      if (!response.ok || !result.success) {
        console.error('❌ Backend returned error:', result);
        throw new Error(result.error || result.message || `HTTP error! status: ${response.status}`);
      }

      setTimeout(() => {
        setShowAppointmentForm(false);
        setIsLoading(false);
        setShowLoadingOverlay(false);

        setShowThankYouModal(true);

        const confirmationMessage = {
          id: Date.now() + 1,
          text: `🎉 Appointment Request Submitted Successfully!

Your appointment has been confirmed and our team will be in touch soon.

Appointment Details:
• Services: ${formData.services.join(', ')}
• Date: ${formData.date}
• Time Slot: ${formatTimeSlotDisplay(formData.time)}
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
      }, 1500);

    } catch (error) {
      console.error('❌ Error saving appointment:', error);
      console.error('❌ Error details:', {
        message: error.message,
        stack: error.stack,
        formData: formData
      });

      setTimeout(() => {
        setShowAppointmentForm(false);
        setIsLoading(false);
        setShowLoadingOverlay(false);

        const isConnectionError = error.message.includes('Could not connect') ||
                                 error.message.includes('fetch') ||
                                 error.message.includes('network');

        const isBusinessHoursError = error.message.includes('business hours');
        const isValidationError = error.message.includes('required') ||
                                 error.message.includes('invalid') ||
                                 error.message.includes('valid');

        let userFriendlyMessage = '';

        if (isBusinessHoursError) {
          const localHours = getLocalBusinessHours();
          const userTz = getUserTimezone();
          const isLocalTime = userTz !== PAKISTAN_TIMEZONE;

          userFriendlyMessage = `⏰ Appointment Time Not Available

The selected time is outside our business hours. Please choose a time during:

🕒 **Business Hours:**
• **Monday - Friday:** ${localHours.weekdays.display}${isLocalTime ? ' (your time)' : ''}
• **Saturday:** ${localHours.saturday.display}${isLocalTime ? ' (your time)' : ''}
• **Sunday:** Closed

${isLocalTime ? 'Original hours: Mon-Fri 6:00 PM - 3:00 AM, Sat 6:00 PM - 10:00 PM (Pakistan Time)\n\n' : ''}Please select a different time and try again.`;
        } else if (isValidationError) {
          userFriendlyMessage = `📝 Appointment Information Issue

Please check your appointment details and ensure all required fields are filled correctly.

You can try submitting your appointment again with the corrected information.`;
        } else if (isConnectionError) {
          userFriendlyMessage = `🔄 Connection Issue

We're experiencing a temporary connection issue. Your appointment information has been noted and our team will contact you directly.

**Your Details:**
• Services: ${formData.services.join(', ')}
• Preferred Date: ${formData.date}
• Preferred Time Slot: ${formatTimeSlotDisplay(formData.time)}
• Contact: ${formData.email}`;
        } else {
          userFriendlyMessage = `⚠️ Appointment Request Received

Your appointment request has been received. Our team will review it and contact you directly to confirm the details.

**Your Details:**
• Services: ${formData.services.join(', ')}
• Preferred Date: ${formData.date}
• Preferred Time Slot: ${formatTimeSlotDisplay(formData.time)}
• Contact: ${formData.email}`;
        }

        const errorMessage = {
          id: Date.now() + 1,
          text: `${userFriendlyMessage}

📧 **Next Steps:**
• Our team will contact you within 24 hours
• You'll receive a confirmation email shortly
• We'll send calendar details once confirmed

Thank you for choosing Techrypt.io! 🚀`,
          sender: 'bot',
          timestamp: new Date()
        };

        setMessages(prev => [...prev, errorMessage]);
        setFormData({ name: '', email: '', phone: '', services: [], date: '', time: '', notes: '' });
        setAppointmentErrors({});
        setError(null);
      }, 1500);
    }
  };



  // MODIFICATION: Conflict resolution functions removed since multiple appointments per time slot are now allowed
  // Original conflict handling functions (commented out):
  // const handleAcceptSuggestedTime = async () => {
  //   if (!conflictData?.suggested_slot) return;
  //   const updatedFormData = {
  //     ...formData,
  //     date: conflictData.suggested_slot.date,
  //     time: conflictData.suggested_slot.time
  //   };
  //   setFormData(updatedFormData);
  //   setShowConflictModal(false);
  //   setConflictData(null);
  //   // Appointment submission logic was here but has been removed
  // };

  // MODIFICATION: Conflict rejection function removed since multiple appointments per time slot are now allowed
  // const handleRejectSuggestedTime = () => {
  //   setShowConflictModal(false);
  //   setConflictData(null);
  //   // Keep the appointment form open for user to choose different time
  // };

  // Open appointment form directly if requested
  useEffect(() => {
    if (isOpen && openAppointmentDirect) {
      setShowContactForm(false);
      setShowAppointmentForm(true);
    }
  }, [isOpen, openAppointmentDirect]);

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
        {!isMinimized && !chatDisabled && (
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
        {/* Show message when chat is disabled due to bot response limit */}
        {chatDisabled && (
          <div className="techrypt-chatbot-limit-message">
            <p>You've reached the maximum number of chatbot responses.<br />Please book an appointment to continue.</p>
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
            <div className="techrypt-form-modal techrypt-appointment-modal" style={{ position: 'relative' }}>
              {/* Loading Overlay for Appointment Form */}
              {showLoadingOverlay && (
                <div className="techrypt-appointment-loading-overlay" style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  right: 0,
                  bottom: 0,
                  backgroundColor: 'rgba(0, 0, 0, 0.7)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  zIndex: 1000,
                  borderRadius: '12px'
                }}>
                  <div className="techrypt-loading-content" style={{
                    textAlign: 'center',
                    color: 'white'
                  }}>
                    <div className="techrypt-loading-spinner" style={{
                      width: '40px',
                      height: '40px',
                      border: '4px solid rgba(255, 255, 255, 0.3)',
                      borderTop: '4px solid #AEBB1E',
                      borderRadius: '50%',
                      animation: 'spin 1s linear infinite',
                      margin: '0 auto 15px auto'
                    }}></div>
                    <p style={{ margin: 0, fontSize: '16px', fontWeight: '500' }}>Processing your appointment...</p>
                  </div>
                </div>
              )}

              <div className="techrypt-form-header text-black">
                <h3 style={{ display: 'flex', alignItems: 'center' }}>
                  <img
                    src={calenderIcon}
                    alt="Calendar Icon"
                    style={{
                      width: '30px',
                      height: '30px',
                      marginRight: '8px'
                    }}
                  />
                  Schedule Your Appointment
                </h3>

                <button onClick={() => setShowAppointmentForm(false)} style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
                  <img src={closeIcon} style={{ width: '20px', height: '20px' }} />
                </button>
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
                        { id: 'branding', name: 'Branding & Logo Design' },
                        { id: 'digital-marketing', name: 'Digital Marketing' },
                        { id: 'web-development', name: 'Web Design & Development' },
                        { id: 'ai-chatbots', name: 'AI & Chatbots' },
                        { id: 'influencer-marketing', name: 'Influencer Marketing' },
                        { id: 'video-production', name: 'Video Production' },
                        { id: 'custom-software', name: 'Custom Software Development' },
                        { id: 'mobile-app', name: 'Mobile App Development' },
                        { id: 'cloud-solutions', name: 'Cloud Solutions' }
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
                              <div className="techrypt-service-icon">
                                <img src={serviceIcons[service.id]} alt={service.name} />
                              </div>
                              <span className="techrypt-service-name">{service.name}</span>
                            </span>
                          </label>
                        </div>
                      ))}
                    </div>
                    {appointmentErrors.services && <span className="techrypt-field-error">{appointmentErrors.services}</span>}
                  </div>

                  <div
                    className="techrypt-business-hours"
                    style={{
                      backgroundColor: '#c4d322',
                      border: '1px solid #0000',
                      borderRadius: '8px',
                      padding: '15px',
                      marginBottom: '15px',
                      fontSize: '13px',
                      lineHeight: '1.4',
                      color: '#000'
                    }}
                  >
                    <h4 style={{ color: '#000', marginBottom: '10px', fontSize: '14px' }}>
                      🕒 Business Hours & Available Times
                    </h4>

                    {(() => {
                      const localHours = getLocalBusinessHours();
                      const userTz = getUserTimezone();
                      const isLocalTime = userTz !== PAKISTAN_TIMEZONE;

                      return (
                        <div>
                          <div>
                            <strong>Monday - Friday:</strong> {localHours.weekdays.display}
                            {isLocalTime && (
                              <span style={{ fontSize: '11px', color: '#64748b' }}> (your time)</span>
                            )}
                          </div>
                          <div>
                            <strong>Saturday:</strong> {localHours.saturday.display}
                            {isLocalTime && (
                              <span style={{ fontSize: '11px', color: '#64748b' }}> (your time)</span>
                            )}
                          </div>
                          <div><strong>Sunday:</strong> Closed</div>

                          {isLocalTime && (
                            <div style={{ fontSize: '11px', color: '#64748b', marginTop: '8px', fontStyle: 'italic' }}>
                              Original: Mon–Fri 6:00 PM – 3:00 AM, Sat 6:00 PM – 10:00 PM (Pakistan Time)
                            </div>
                          )}

                          <p style={{ fontSize: '12px', color: '#64748b', marginTop: '8px', marginBottom: '0' }}>
                            Our team will reach out within the selected time interval
                          </p>
                        </div>
                      );
                    })()}
                  </div>


                  <div className="techrypt-form-row">
                    <div className="techrypt-form-field">
                      <label>Preferred Date *</label>
                      <input
                        type="date"
                        value={formData.date}
                        onChange={(e) => {
                          setFormData(prev => ({
                            ...prev,
                            date: e.target.value,
                            time: '' // Clear time when date changes
                          }));
                          if (appointmentErrors.date) {
                            setAppointmentErrors(prev => ({ ...prev, date: '' }));
                          }
                          if (appointmentErrors.time) {
                            setAppointmentErrors(prev => ({ ...prev, time: '' }));
                          }
                        }}
                        min={new Date().toISOString().split('T')[0]}
                        className={appointmentErrors.date ? 'error' : ''}
                        required
                      />
                      {appointmentErrors.date && <span className="techrypt-field-error">{appointmentErrors.date}</span>}
                    </div>
                    <div className="techrypt-form-field">
                      <label>Preferred Time *</label>
                      <select
                        value={formData.time}
                        onChange={(e) => {
                          setFormData(prev => ({ ...prev, time: e.target.value }));
                          if (appointmentErrors.time) {
                            setAppointmentErrors(prev => ({ ...prev, time: '' }));
                          }
                        }}
                        className={appointmentErrors.time ? 'error' : ''}
                        required
                        disabled={formData.date && isSelectedDateSunday()}
                      >
                        <option value="">
                          {formData.date && isSelectedDateSunday()
                            ? "Closed on Sundays"
                            : (() => {
                                // Check if all time slots are in the past for today
                                const selectedDate = new Date(formData.date);
                                const today = new Date();
                                today.setHours(0, 0, 0, 0);
                                
                                if (selectedDate.getTime() === today.getTime()) {
                                  const allTimeSlots = ["6pm-9pm", "9pm-12am", "12am-3am"];
                                  const allPast = allTimeSlots.every(slot => isTimeSlotInPast(slot));
                                  
                                  if (allPast) {
                                    return "All time slots for today have passed";
                                  }
                                }
                                
                                return "Select a time";
                              })()
                          }
                        </option>
                        {!isSelectedDateSunday() &&
                          <>
                            <option 
                              value="6pm-9pm" 
                              disabled={isTimeSlotInPast("6pm-9pm")}
                              style={isTimeSlotInPast("6pm-9pm") ? {color: '#999', backgroundColor: '#f5f5f5'} : {}}
                            >
                              6:00 PM – 9:00 PM {isTimeSlotInPast("6pm-9pm") ? "(Past)" : ""}
                            </option>
                            <option 
                              value="9pm-12am" 
                              disabled={isTimeSlotInPast("9pm-12am")}
                              style={isTimeSlotInPast("9pm-12am") ? {color: '#999', backgroundColor: '#f5f5f5'} : {}}
                            >
                              9:00 PM – 12:00 AM {isTimeSlotInPast("9pm-12am") ? "(Past)" : ""}
                            </option>
                            <option 
                              value="12am-3am" 
                              disabled={isTimeSlotInPast("12am-3am")}
                              style={isTimeSlotInPast("12am-3am") ? {color: '#999', backgroundColor: '#f5f5f5'} : {}}
                            >
                              12:00 AM – 3:00 AM {isTimeSlotInPast("12am-3am") ? "(Past)" : ""}
                            </option>
                          </>
                        }
                      </select>
                      {appointmentErrors.time && <span className="techrypt-field-error">{appointmentErrors.time}</span>}

                      {/* Sunday message */}
                      {formData.date && isSelectedDateSunday() && (
                        <div className="techrypt-sunday-message" style={{
                          marginTop: '8px',
                          padding: '10px',
                          backgroundColor: '#fef3c7',
                          border: '1px solid #f59e0b',
                          borderRadius: '6px',
                          color: '#92400e',
                          fontSize: '14px'
                        }}>
                          ⚠️ We are closed on Sundays. Please select another day for your appointment.
                        </div>
                      )}

                      {/* Past time slots message for today */}
                      {formData.date && !isSelectedDateSunday() && (() => {
                        const selectedDate = new Date(formData.date);
                        const today = new Date();
                        today.setHours(0, 0, 0, 0);
                        
                        if (selectedDate.getTime() === today.getTime()) {
                          const allTimeSlots = ["6pm-9pm", "9pm-12am", "12am-3am"];
                          const allPast = allTimeSlots.every(slot => isTimeSlotInPast(slot));
                          
                          if (allPast) {
                            return (
                              <div className="techrypt-past-slots-message" style={{
                                marginTop: '8px',
                                padding: '10px',
                                backgroundColor: '#fef2f2',
                                border: '1px solid #f87171',
                                borderRadius: '6px',
                                color: '#dc2626',
                                fontSize: '14px'
                              }}>
                                ⏰ All time slots for today have passed. Please select a future date for your appointment.
                              </div>
                            );
                          }
                        }
                        return null;
                      })()}

                      {/* No time slots available message */}
                      {formData.date && !isSelectedDateSunday() && getAvailableTimeSlots().length === 0 && (
                        <div className="techrypt-no-slots-message" style={{
                          marginTop: '8px',
                          padding: '10px',
                          backgroundColor: '#fef2f2',
                          border: '1px solid #f87171',
                          borderRadius: '6px',
                          color: '#dc2626',
                          fontSize: '14px'
                        }}>
                          ⚠️ No time slots available for this date. Please select a different date.
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="techrypt-form-field">
                    <label>Additional Notes (Optional)</label>
                    <textarea
                      value={formData.notes}
                      onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
                      placeholder="What are your goals?"
                      rows="3"
                    />
                  </div>
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

        {/* MODIFICATION: Conflict resolution modal removed since multiple appointments per time slot are now allowed */}

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
                  <h4 className="text-xl font-bold text-white mb-2">Thanks! You're booked.</h4>
                  <p className="text-gray-300 mb-4">
                    You'll receive a confirmation email and meet our strategist at the time you chose.
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
                
                <div className="techrypt-form-actions" style={{ gap: '10px' }}>
                  <button
                    className="techrypt-form-cancel"
                    onClick={() => {
                      setShowThankYouModal(false);
                      // Navigate to About Us page
                      window.open('/about', '_blank');
                    }}
                    style={{ flex: 1 }}
                  >
                    Learn More
                  </button>
                  <button
                    className="techrypt-form-submit"
                    onClick={() => setShowThankYouModal(false)}
                    style={{ flex: 1 }}
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
