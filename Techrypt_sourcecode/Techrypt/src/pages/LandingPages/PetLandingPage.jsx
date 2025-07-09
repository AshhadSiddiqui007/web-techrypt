import React, { useState } from 'react';
import { motion } from 'framer-motion';
import HeroSection from '../../components/PetLandingPage/HeroSection';
import WhyLoveUsSection from '../../components/PetLandingPage/WhyLoveUs';
import BenefitsSection from '../../components/PetLandingPage/Benefits';
import ComparisonSection from '../../components/PetLandingPage/Comparisons';
import TestimonialsSection from '../../components/PetLandingPage/Testimonials';
import FAQSection from '../../components/PetLandingPage/FAQ';
import CTASection from '../../components/PetLandingPage/CTA';
import PetChatUI from '../../components/PetLandingPage/PetChatUI';

const PetLandingPage = () => {
  const [activeAccordion, setActiveAccordion] = useState(null);
  const [bookingModalOpen, setBookingModalOpen] = useState(false);

  const toggleAccordion = (index) => {
    setActiveAccordion(activeAccordion === index ? null : index);
  };

  const openBookingModal = () => {
    setBookingModalOpen(true);
  };

  const closeBookingModal = () => {
    setBookingModalOpen(false);
  };

  const fadeInUp = {
    initial: { opacity: 0, y: 60 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6, ease: "easeOut" }
  };

  const staggerContainer = {
    animate: {
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const handleGetStarted = () => {
    // Trigger the pet-specific chatbot to open with a welcome message
    const event = new CustomEvent('openPetChatbot', {
      detail: {
        contextMessage: "🐾 Welcome to our pet care automation platform! I'm here to help you streamline your pet business. What can I help you with today?",
        businessType: 'Pet Business',
        businessProfile: 'pets',
        showAppointmentForm: true
      }
    });
    window.dispatchEvent(event);
  };

  return (
    <div className="min-h-screen bg-dark text-white font-inter overflow-x-hidden">
      <HeroSection 
        onGetStarted={handleGetStarted} 
        fadeInUp={fadeInUp} 
        staggerContainer={staggerContainer} 
      />
      <WhyLoveUsSection 
        fadeInUp={fadeInUp} 
        staggerContainer={staggerContainer} 
      />
      <BenefitsSection />
      <ComparisonSection />
      <TestimonialsSection 
        fadeInUp={fadeInUp} 
        staggerContainer={staggerContainer} 
      />
      <FAQSection 
        activeAccordion={activeAccordion} 
        toggleAccordion={toggleAccordion} 
        fadeInUp={fadeInUp} 
        staggerContainer={staggerContainer} 
      />
      <CTASection 
        openBookingModal={openBookingModal} 
      />
    </div>
  );
};

export default React.memo(PetLandingPage);