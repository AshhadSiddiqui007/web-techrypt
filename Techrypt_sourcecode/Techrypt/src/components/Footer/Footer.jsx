import React, { useState } from 'react';
import { FaLinkedin, FaYoutube, FaFacebookSquare, FaTwitter } from 'react-icons/fa';
import { RiArrowUpDoubleLine, RiInstagramFill } from 'react-icons/ri';
import { motion } from 'framer-motion';
import { clutch, google, meta } from '../../assets/mainImages';
import techryptLogo from "../../assets/Images/techryptLogo.png";
import ContactForm from '../ContactForm/ContactForm';
import TopModal from '../TopModal/TopModal';
import PrivacyPolicy from '../PrivacyPolicy/PrivacyPolicy';
import { Link, useLocation } from 'react-router-dom';
// Import the Newsletterbox component
import Newsletterbox from './Newsletterbox';


const Footer = () => {
  const location = useLocation()
  const [privacy, setPrivacy] = useState(false);
  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  };

  // Add state for form fields
  const [formData, setFormData] = useState({
    name: '',
    company: '',
    email: '',
    source: '',
    goals: ''
  });

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Function to trigger appointment booking
  const handleSubmit = () => {
    // Use the exact appointment trigger pattern from TechryptChatbot.jsx
    const messageText = "I want to book an appointment";
    
    // Create a user message to simulate typing "I want to book an appointment"
    const userMessage = {
      id: Date.now(),
      text: messageText,
      sender: 'user',
      timestamp: new Date()
    };
    
    // Dispatch the event that will open the chatbot
    const event = new CustomEvent('openTechryptChatbot', {
      detail: {
        contextMessage: messageText,
        businessType: 'Form Submission',
        showAppointmentForm: true,
        autoMessage: messageText
      }
    });
    window.dispatchEvent(event);
  };

  return (
    <div className="text-center bg-[#000] overflow-x-hidden pt-12 md:pt-24 px-4 md:px-6">
      <div className="inline-flex flex-col items-center justify-center mb-8 md:mb-12">
        <img className="mx-auto object-contain w-48 md:w-72 mb-2 pb-4 md:pb-8" src={techryptLogo} alt="Techrypt Logo" />
        <h3 className="text-sm md:text-lg font-bold text-white mt-2 px-3 md:px-5 py-2 border-2 border-white rounded-full inline-block text-center">
          Empowering Digital Skills & AI-Driven Business Solutions
        </h3>
        <div className="w-full h-16 md:h-24 pt-4 md:pt-8 flex justify-center">
          <motion.div
            className="bg-white w-0.5"
            initial={{ height: 0 }}
            whileInView={{ height: '60px' }}
            viewport={{ once: false }}
            transition={{ duration: 0.8, ease: 'easeOut', delay: 0.3 }}
          />
        </div>
      </div>

      {/*Enhanced Mobile-Responsive Contact Form*/}
      <div className="max-w-3xl mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 mb-4 md:mb-6">
          <div>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              placeholder="Your Name"
              className="w-full bg-transparent border-b border-gray-600 py-3 px-3 text-white focus:outline-none focus:border-primary text-base md:text-lg transition-colors duration-300"
            />
          </div>
          <div>
            <input
              type="text"
              placeholder="Your Company name"
              className="w-full bg-transparent border-b border-gray-600 py-3 px-3 text-white focus:outline-none focus:border-primary text-base md:text-lg transition-colors duration-300"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 mb-4 md:mb-6">
          <div>
            <input
              type="email"
              placeholder="Your Email"
              className="w-full bg-transparent border-b border-gray-600 py-3 px-3 text-white focus:outline-none focus:border-primary text-base md:text-lg transition-colors duration-300"
            />
          </div>
          <div>
            <select
              className="w-full bg-transparent border-b border-gray-600 py-3 px-3 text-gray-400 focus:outline-none focus:border-primary text-base md:text-lg transition-colors duration-300"
            >
              <option value="">How Did You Hear About Us</option>
              <option value="google">Google</option>
              <option value="social">Social Media</option>
              <option value="referral">Referral</option>
              <option value="other">Other</option>
            </select>
          </div>
        </div>

        <div className="mb-6 md:mb-8">
          <textarea
            placeholder="What is the biggest challenge with your business right now?"
            rows="3"
            className="w-full bg-transparent border-b border-gray-600 py-3 px-3 text-white focus:outline-none focus:border-primary text-base md:text-lg transition-colors duration-300 resize-none"
          ></textarea>
        </div>

        <div className="flex justify-center items-center my-8">
          <button
            onClick={handleSubmit}
            className="bg-primary hover:bg-primary/90 text-black font-bold py-3 md:py-4 px-6 md:px-8 rounded-full text-base md:text-lg transition-all duration-300 transform hover:scale-105 touch-target"
          >
            Submit
          </button>
        </div>
      </div>

      <div className="relative top-5 flex flex-col text-gray-400 mb-12 leading-8">
        <span>
          By clicking submit, you agree to our{' '}
          <Link to={"/PrivacyPolicy"} className=" text-primary">
            Privacy Policy
          </Link>
        </span>
        <span> 
          {' '} and{' '}
          <Link to={"Terms&Conditions"} className="text-primary">
            Terms and Conditions
          </Link>
        </span>
      </div>

      <div className="flex gap-6 md:gap-10 lg:gap-20 justify-center items-center my-8 md:my-12">
        <a href="https://www.linkedin.com/company/techrypt-io/posts/?feedView=all" target="_blank" rel="noopener noreferrer" className="touch-target">
          <FaLinkedin className="text-3xl md:text-4xl text-white glowing-green transition-all duration-300 hover:scale-110" />
        </a>

        <a href="/" className="touch-target">
          <FaYoutube className="text-3xl md:text-4xl text-white glowing-green transition-all duration-300 hover:scale-110" />
        </a>
        <a href="https://www.instagram.com/tech.rypt/" className="touch-target">
          <RiInstagramFill className="text-3xl md:text-4xl text-white glowing-green transition-all duration-300 hover:scale-110" />
        </a>
        <a href="https://www.facebook.com/people/Techrypt/61575440404641/#" className="touch-target">
          <FaFacebookSquare className="text-3xl md:text-4xl text-white glowing-green transition-all duration-300 hover:scale-110" />
        </a>
        <a href="/" className="touch-target">
          <FaTwitter className="text-3xl md:text-4xl text-white glowing-green transition-all duration-300 hover:scale-110" />
        </a>
      </div>

      {/* Footer Lower Section */}
      <div className="w-full mt-4">
        <div className="flex flex-col md:flex-row items-center justify-between max-w-7xl mx-auto px-4">
          {/* Centered left section */}
          <div className="flex flex-row items-center justify-center gap-3 w-full md:w-auto">
            <a
              href="mailto:INFO@TECHRYPT.IO"
              className="text-gray-400 glowing-green hover:text-primary transition-colors duration-300 text-xs md:text-sm whitespace-nowrap"
            >
              INFO@TECHRYPT.IO
            </a>
            <Newsletterbox />
          </div>
          {/* Right: Privacy/Terms */}
          <div className="flex flex-row items-center gap-4 mt-2 md:mt-0">
            <Link to="/PrivacyPolicy" className="hover:text-primary transition-colors duration-300 text-gray-400 text-xs md:text-sm">
              Privacy Policy
            </Link>
            <Link to="/Terms&Conditions" className="hover:text-primary transition-colors duration-300 text-gray-400 text-xs md:text-sm">
              Terms & Conditions
            </Link>
          </div>
        </div>
        {/* Powered by (centered, lowest) */}
        <div className="w-full flex justify-center items-center py-2">
          <span className="text-white glowing-green text-sm md:text-base">Powered by Techrypt.io</span>
        </div>
      </div>

      {/* <TopModal isOpen={privacy} onClose={() => setPrivacy(false)}>
        <PrivacyPolicy />
      </TopModal> */}
    </div>
  );
};

export default Footer;
