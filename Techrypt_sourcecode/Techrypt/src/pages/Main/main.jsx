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
import { useState } from 'react';

// Interactive Button component defined outside the main component
const InteractiveButton = ({ onClick }) => {
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    setMousePos({ x, y });
  };

  return (
    <div
      className="absolute inset-x-0 flex justify-center z-50"
      style={{
        top: 'calc(80vh - 100px)',
        padding: 'clamp(1rem, 4vw, 2rem)' /* Proportional padding */
      }}
    >
      <motion.button
        className="relative overflow-hidden text-black rounded-lg font-semibold transition-all duration-300 group touch-target"
        style={{
          background: `linear-gradient(135deg, #2a2a2a 0%, #404040 20%, #5a5a5a 40%, #A8B91A 70%, #C4D322 100%), radial-gradient(circle at ${mousePos.x}% ${mousePos.y}%, #E5F72E 0%, #C4D322 25%, #A8B91A 50%, #C4D322 100%)`,
          backgroundBlendMode: 'overlay',
          padding: 'clamp(0.75rem, 3vw, 1.5rem) clamp(1.5rem, 6vw, 3rem)', /* Proportional padding */
          fontSize: 'clamp(0.875rem, 2.5vw, 1.125rem)', /* Proportional font size */
          minHeight: 'clamp(48px, 8vh, 64px)', /* Proportional height */
          width: 'clamp(280px, 60vw, 400px)', /* Proportional width */
          maxWidth: '90vw' /* Prevent overflow on small screens */
        }}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={onClick}
        onMouseMove={handleMouseMove}
        weight={700}
      >
        {/* Animated gradient overlay */}
        <div
          className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
          style={{
            background: `radial-gradient(circle 150px at ${mousePos.x}% ${mousePos.y}%, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0.1) 30%, transparent 70%)`
          }}
        />

        {/* Button text */}
        <span className="relative z-10 font-bold">
          GET YOUR AUTOMATION TODAY
        </span>
      </motion.button>
    </div>
  );
};

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
      
      {/* Interactive button with gradient cursor effect */}
      <InteractiveButton onClick={handleGetStarted} />
      
      <div className="fading"></div>
      
      <AgencyDetails />
      <CreativeTeamSection />
      <SliderLogo />
      <Services className={"z-20"} />
    </div>
  );
};

export default main;