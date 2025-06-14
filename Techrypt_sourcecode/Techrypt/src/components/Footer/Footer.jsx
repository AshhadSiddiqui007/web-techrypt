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
    <div className="text-center bg-[#000] mt-10 overflow-x-hidden pt-24 px-3">
      <div className="inline-flex flex-col items-center justify-center mb-12">
        <img className="mx-auto object-contain w-72 mb-2 pb-8" src={techryptLogo} alt="Techrypt Logo" />
        <h3 className="text-lg font-bold text-white mt-2 px-5 py-2 border-2 border-white rounded-full inline-block">
          Empowering Digital Skills & AI-Driven Business Solutions
        </h3>
        <div className="w-full h-24 pt-8 flex justify-center">
          <motion.div
            className="bg-white w-0.5"
            initial={{ height: 0 }}
            whileInView={{ height: '100px' }}
            viewport={{ once: false }}
            transition={{ duration: 0.8, ease: 'easeOut', delay: 0.3 }}
          />
        </div>
      </div>

      {/*Place form here*/}
      <div className="max-w-3xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div>
            <input 
              type="text" 
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              placeholder="Your Name" 
              className="w-full bg-transparent border-b border-gray-600 py-2 px-3 text-white focus:outline-none focus:border-primary"
            />
          </div>
          <div>
            <input 
              type="text" 
              placeholder="Your Company name" 
              className="w-full bg-transparent border-b border-gray-600 py-2 px-3 text-white focus:outline-none focus:border-primary"
            />
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div>
            <input 
              type="email" 
              placeholder="Your Email" 
              className="w-full bg-transparent border-b border-gray-600 py-2 px-3 text-white focus:outline-none focus:border-primary"
            />
          </div>
          <div>
            <select 
              className="w-full bg-transparent border-b border-gray-600 py-2 px-3 text-gray-400 focus:outline-none focus:border-primary"
            >
              <option value="">How Did You Hear About Us</option>
              <option value="google">Google</option>
              <option value="social">Social Media</option>
              <option value="referral">Referral</option>
              <option value="other">Other</option>
            </select>
          </div>
        </div>
        
        <div className="mb-8">
          <textarea 
            placeholder="What is the biggest challenge with your business right now?" 
            rows="3" 
            className="w-full bg-transparent border-b border-gray-600 py-2 px-3 text-white focus:outline-none focus:border-primary"
          ></textarea>
        </div>
        
        <div className="text-center">
          <button 
            onClick={handleSubmit}
            className="bg-primary hover:bg-primary/90 text-black font-bold py-3 px-8 rounded-full"
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

      <div className="flex gap-4 md:gap-10 lg:gap-20 justify-center items-center">
        <a href="https://www.linkedin.com/company/techrypt-io/posts/?feedView=all" target="_blank" rel="noopener noreferrer">
          <FaLinkedin className="text-4xl text-white glowing-green transition-all duration-150" />
        </a>

        <a href="/">
          <FaYoutube className="text-4xl text-white glowing-green transition-all duration-150" />
        </a>
        <a href="https://www.instagram.com/tech.rypt/">
          <RiInstagramFill className="text-4xl text-white glowing-green transition-all duration-150" />
        </a>
        <a href="https://www.facebook.com/people/Techrypt/61575440404641/#">
          <FaFacebookSquare className="text-4xl text-white glowing-green transition-all duration-150" />
        </a>
        <a href="/">
          <FaTwitter className="text-4xl text-white glowing-green transition-all duration-150" />
        </a>
      </div>



      <div className="flex md:px-20 py-3 px-2 max-md:flex-col items-center md:items-end justify-between gap-3 w-full mb-2">

      <div className="flex flex-col items-center justify-start gap-5 max-md:order-3 max-md:mt-7">
        <div
          className="h-10 md:w-16 w-10 md:h-16 flex justify-center items-center text-5xl text-primary cursor-pointer rounded-full border border-primary hover:bg-primary hover:text-white glowing-yellow transition-all duration-300"
          title='Scroll to top'
          onClick={scrollToTop}
        >
          <RiArrowUpDoubleLine />
        </div>
        <a href="mailto:INFO@TECHRYPT.IO" className="text-gray-400 text-xs glowing-green">
          INFO@TECHRYPT.IO
        </a>
      </div>

      <div className="flex flex-col items-center justify-center w-full text-center">
        <p
          className="text-white glowing-green"
          style={{
            display: 'flex',
            justifyContent: 'center',  // Horizontally center
            textAlign: 'center',       // Center text inside the element
            width: '100%',             // Take full width of its container
            marginLeft: '100px'
          }}
        >
          Powered by Techrypt.io
        </p>
      </div>

      <div className="flex gap-10 justify-center text-gray-400">
        <Link to={"/PrivacyPolicy"} onClick={() => setPrivacy(true)} className="">
          Privacy Policy
        </Link>
        <Link to={"/Terms&Conditions"} className="ml-1">
          Terms & Conditions
        </Link>
      </div>

    </div>

      {/* <TopModal isOpen={privacy} onClose={() => setPrivacy(false)}>
        <PrivacyPolicy />
      </TopModal> */}
    </div>
  );
};

export default Footer;
