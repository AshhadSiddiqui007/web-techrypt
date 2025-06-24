import React from 'react';
import './PRLandingPage.css';
import HeroSection from '../../components/PRLandingPage/HeroSection';
import FeaturesSection from '../../components/PRLandingPage/Features';
import PricingSection from '../../components/PRLandingPage/Pricing';
import CTASection from '../../components/PRLandingPage/CTA';
import TalkingBubble from '../../components/PRLandingPage/TalkingBubble';

const PRLandingPage = () => {

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
    <div className="pr-landing-root">
      <div className="pr-broadcast-anim">
        <span className="pr-broadcast-center"></span>
        <span className="pr-broadcast-wave wave1"></span>
        <span className="pr-broadcast-wave wave2"></span>
      </div>
      <div className="pr-broadcast-creative">
        <div className="pr-megaphone">
          <div className="pr-megaphone-mouth"></div>
          <div className="pr-megaphone-handle"></div>
        </div>
        <span className="pr-broadcast-wave-creative"></span>
        <span className="pr-broadcast-wave-creative wave2"></span>
        <span className="pr-broadcast-wave-creative wave3"></span>
      </div>
      <HeroSection />
      <FeaturesSection />
      <PricingSection />
      <CTASection onGetStarted={handleGetStarted} />
      <TalkingBubble />
    </div>
  );
};

export default React.memo(PRLandingPage);