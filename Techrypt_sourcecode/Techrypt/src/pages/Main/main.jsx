import React from "react";
import Hero from "../../components/Hero/Hero";
import AgencyDetails from "../../components/AgencyDetails/AgencyDetails";
import SliderLogo from "../../components/SliderLogos/AutoSlider";
import CreativeTeamSection from "../../components/CreativeTeamSection/CreativeTeamSection.jsx";
import VideoGallery from "../../components/VideoGallery/VideoGallery.jsx";
import Verticals from "../../components/Verticals/Verticals.jsx";
import Services from "../../components/WhatWeDo/Services.jsx";
import ParallaxWrapper from "../../components/ParallaxWrapper/ParallaxWrapper.jsx";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";

const main = () => {
  const handleGetStarted = () => {
    // Directly trigger the chatbot to open with a welcome message
    const event = new CustomEvent('openTechryptChatbot', {
      detail: {
        contextMessage: "Hi there! I'd be happy to help you take your business to the next level. Could you share some information about yourself so I can provide personalized assistance?",
        businessType: 'New Visitor',
        showAppointmentForm: true
      }
    });
    window.dispatchEvent(event);
  };

  return (
    <div className="relative">
      <Hero title={["Development", "Branding", "Marketing"]} text={" Unlock new opportunities with expert-led training & cutting-edge digital services.Techrypt.io is a forward-thinking team on a mission to revolutionize how individuals learn and how businesses grow."} />
      
      {/* Get Started Button */}
      <div className="absolute inset-x-0 flex justify-center z-50" style={{ top: 'calc(80vh - 100px)' }}>
        <motion.button
          className="bg-primary text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary/90 transition-colors"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleGetStarted}
        >
          Take Your Business to the <br />Next Level
        </motion.button>
      </div>
      
      <div className="fading"></div>
      <AgencyDetails />
      <CreativeTeamSection />

      {/* <VideoGallery /> */}
      <SliderLogo />
      <Services className={"z-20"} />
      <Verticals />
      
      
  
    
    </div>
  );
};

export default main;
