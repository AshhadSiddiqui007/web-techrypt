import React, { useState } from "react";
import { motion } from "framer-motion";
import mask1 from "../../assets/svgs/mask1.svg";
import mask2 from "../../assets/svgs/mask2.svg";
import mask3 from "../../assets/svgs/mask3.svg";
import mask4 from "../../assets/svgs/mask4.svg";
import mask5 from "../../assets/svgs/mask5.svg";
import VerticlesCard from "../VerticlesCard/VerticlesCard.jsx";
import "./Verticals.css"; // Import the CSS file



export default function Verticals() {
  const handleGetStarted = () => {
    const event = new CustomEvent('openTechryptChatbot', {
      detail: {
        contextMessage: "Hi there! I'd be happy to help you take your business to the next level. Could you share some information about yourself so I can provide personalized assistance?",
        businessType: 'New Visitor',
        showAppointmentForm: true
      }
    });
    window.dispatchEvent(event);
  };
  const [customMessage, setCustomMessage] = useState("");

  const verticals = [
    {
      text: "E-commerce",
      class: mask1,
      type: "large",
      subtitle: "Solutions",
      description: "Complete digital commerce platforms",
      showVisual: "ecommerce"
    },
    {
      text: "Don't see your",
      class: mask2,
      type: "medium",
      subtitle: "Industry?",
      description: "Custom solutions for any sector",
      isSpecial: true
    },
    {
      text: "Education",
      class: mask3,
      type: "medium",
      subtitle: "Technology",
      description: "Learning management systems",
      showVisual: "education"
    },
    {
      text: "Fashion",
      class: mask2,
      type: "medium",
      subtitle: "Industry",
      description: "Style and trend platforms",
      showVisual: "fashion"
    },
    {
      text: "Travel",
      class: mask4,
      type: "medium",
      subtitle: "Services",
      description: "Booking and management systems",
      showVisual: "travel"
    },
    {
      text: "Finance",
      class: mask5,
      type: "medium",
      subtitle: "Solutions",
      description: "Secure financial platforms",
      showVisual: "chart"
    },
    {
      text: "Pet Industry",
      class: mask2,
      type: "medium",
      subtitle: "Care",
      description: "Pet care and service platforms",
      showVisual: "pet"
    },
    {
      text: "Health",
      class: mask3,
      type: "medium",
      subtitle: "Tech",
      description: "Healthcare management systems",
      showVisual: "mobile"
    },
    {
      text: "Entertainment",
      class: mask5,
      type: "wide",
      subtitle: "Platforms",
      description: "Media and content distribution",
      showVisual: "social"
    },
  ];

  const getCardClasses = (type) => {
    switch(type) {
      case 'large':
        return 'col-span-1 md:col-span-2 row-span-1 md:row-span-2';
      case 'wide':
        return 'col-span-1 md:col-span-2';
      case 'small':
        return 'col-span-1';
      default: // This will catch 'medium' and apply default sizing
        return 'col-span-1';
    }
  };

  const getCardStyles = (type) => {
    switch(type) {
      case 'large':
        return { minHeight: 'clamp(300px, 40vh, 500px)' }; /* Proportional large card */
      case 'wide':
        return { minHeight: 'clamp(200px, 25vh, 300px)' }; /* Proportional wide card */
      case 'small':
        return { minHeight: 'clamp(150px, 20vh, 250px)' }; /* Proportional small card */
      default:
        return { minHeight: 'clamp(200px, 25vh, 300px)' }; /* Proportional medium card */
    }
  };

  const cardAnimation = {
    hidden: { opacity: 0, scale: 0.8, y: 20 },
    visible: (i) => ({
      opacity: 1,
      scale: 1,
      y: 0,
      transition: {
        type: "spring",
        stiffness: 100,
        damping: 10,
        duration: 0.6,
        delay: i * 0.1
      }
    })
  };

  const ShoppingCartVisual = () => (
  <div className="absolute bottom-6 right-6 opacity-60">
    <div className="bg-primary/20 rounded-xl w-32 h-32 flex items-center justify-center">
      <div className="w-20 h-20 relative">
        {/* Main cart body */}
          <div className="w-16 h-10 border-4 border-primary/60 rounded-t-2xl"></div>
          
          {/* Cart wheels */}
          <div className="absolute bottom-0 left-2 w-4 h-8 border-4 border-primary/60 rounded-full"></div>
          <div className="absolute bottom-0 right-2 w-4 h-8 border-4 border-primary/60 rounded-full"></div>
          
          {/* Cart handle */}
          <div className="absolute top-4 right-0 w-8 h-12 border-4 border-primary/60 rounded-r-xl"></div>
          
          {/* Cart items (optional decorative elements) */}
          <div className="absolute top-2 left-2 w-3 h-3 bg-primary/40 rounded"></div>
          <div className="absolute top-2 left-6 w-2 h-4 bg-primary/40 rounded"></div>
          <div className="absolute top-2 left-9 w-4 h-2 bg-primary/40 rounded"></div>
        </div>
      </div>
    </div>
  );

  const EducationVisual = () => (
    <div className="absolute bottom-6 right-6 opacity-30">
      <div className="bg-primary/20 rounded-lg w-16 h-16 flex items-center justify-center">
        <div className="w-12 h-8 relative">
          <div className="w-12 h-2 bg-primary/60 absolute bottom-0"></div>
          <div className="w-8 h-6 bg-primary/50 absolute bottom-2 left-2 rounded-t-lg"></div>
          <div className="w-4 h-1 bg-primary/70 absolute top-0 left-4 rounded"></div>
        </div>
      </div>
    </div>
  );

  const FashionVisual = () => (
    <div className="absolute bottom-6 right-6 opacity-30">
      <div className="bg-primary/20 rounded-lg w-16 h-16 flex items-center justify-center">
        <div className="w-10 h-10 relative">
          <div className="w-8 h-1 bg-primary/60 absolute top-0 left-1 rounded"></div>
          <div className="w-1 h-8 bg-primary/60 absolute top-1 left-4.5 rounded"></div>
          <div className="w-6 h-6 border-2 border-primary/50 absolute bottom-0 left-2 rounded-b-lg"></div>
        </div>
      </div>
    </div>
  );

  const TravelVisual = () => (
    <div className="absolute bottom-6 right-6 opacity-30">
      <div className="bg-primary/20 rounded-lg w-16 h-16 flex items-center justify-center">
        <div className="w-12 h-10 relative">
          <div className="w-10 h-2 bg-primary/60 absolute bottom-0 left-1 rounded"></div>
          <div className="w-8 h-6 bg-primary/50 absolute bottom-2 left-2 rounded"></div>
          <div className="w-4 h-1 bg-primary/70 absolute top-1 left-4 rounded transform -rotate-45"></div>
          <div className="w-6 h-1 bg-primary/70 absolute top-3 left-3 rounded transform rotate-45"></div>
        </div>
      </div>
    </div>
  );

  const PetVisual = () => (
    <div className="absolute bottom-6 right-6 opacity-30">
      <div className="bg-primary/20 rounded-lg w-16 h-16 flex items-center justify-center">
        <div className="w-12 h-12 relative">
          <div className="w-3 h-3 bg-primary/60 absolute top-0 left-1 rounded-full"></div>
          <div className="w-3 h-3 bg-primary/60 absolute top-0 right-1 rounded-full"></div>
          <div className="w-4 h-4 bg-primary/50 absolute bottom-1 left-4 rounded-full"></div>
          <div className="w-2 h-2 bg-primary/60 absolute bottom-4 left-2 rounded-full"></div>
          <div className="w-2 h-2 bg-primary/60 absolute bottom-4 right-2 rounded-full"></div>
        </div>
      </div>
    </div>
  );

  const ChartVisual = () => (
    <div className="absolute bottom-6 right-6 opacity-40">
      <div className="flex space-x-1 items-end h-12 w-16">
        <div className="bg-primary rounded-sm w-3 h-6"></div>
        <div className="bg-primary/80 rounded-sm w-3 h-8"></div>
        <div className="bg-primary/90 rounded-sm w-3 h-10"></div>
        <div className="bg-primary/70 rounded-sm w-3 h-4"></div>
      </div>
      <div className="text-primary text-xs font-bold mt-1">↗ Growth</div>
    </div>
  );

  const MobileVisual = () => (
    <div className="absolute bottom-6 right-6 opacity-60">
      <div className="bg-primary/20 rounded-lg w-12 h-20 p-1">
        <div className="bg-primary/40 rounded w-full h-3 mb-1"></div>
        <div className="bg-primary/30 rounded w-full h-1 mb-1"></div>
        <div className="bg-primary/30 rounded w-3/4 h-1 mb-1"></div>
        <div className="bg-primary/50 rounded w-full h-4"></div>
      </div>
    </div>
  );

  const SocialVisual = () => (
    <div className="absolute bottom-6 right-6 opacity-40">
      <div className="flex space-x-2">
        <div className="w-6 h-6 bg-primary/60 rounded-lg"></div>
        <div className="w-6 h-6 bg-primary/50 rounded-lg"></div>
        <div className="w-6 h-6 bg-primary/70 rounded-lg"></div>
        <div className="w-6 h-6 bg-primary/40 rounded-lg"></div>
      </div>
    </div>
  );

  const renderVisual = (type) => {
    switch(type) {
      case 'ecommerce': return <ShoppingCartVisual />;
      case 'chart': return <ChartVisual />;
      case 'mobile': return <MobileVisual />;
      case 'social': return <SocialVisual />;
      case 'education': return <EducationVisual />;
      case 'fashion': return <FashionVisual />;
      case 'travel': return <TravelVisual />;
      case 'pet': return <PetVisual />;
      default: return null;
    }
  };

  const handleSendMessageToChatbot = () => {
    if (customMessage.trim() === "") {
      console.log("Attempted to send empty message. Chatbot not triggered.");
      return;
    }
    console.log("Dispatching chatbot event with message:", customMessage);
    const event = new CustomEvent('openTechryptChatbot', {
      detail: {
        contextMessage: customMessage,
        businessType: 'Custom Industry Inquiry',
        autoSendMessage: true
      }
    });
    window.dispatchEvent(event);
    setCustomMessage("");
  };

  // Separate the "Pet Industry", "Health", and "Entertainment" cards
  const petIndustryCard = verticals.find(item => item.text === "Pet Industry");
  const healthCard = verticals.find(item => item.text === "Health");
  const entertainmentCard = verticals.find(item => item.text === "Entertainment");

  // Filter out these three cards from the main list for rendering in their specific row
  const remainingVerticals = verticals.filter(item =>
    item.text !== "Pet Industry" &&
    item.text !== "Health" &&
    item.text !== "Entertainment"
  );

  // Create a custom component for the E-commerce card
  const EcommerceCard = ({ itemData }) => (
    <VerticlesCard
      foldSize={50}
      className="w-full h-full backdrop-blur-sm border border-primary/20 bg-[#D8E35A] bg-opacity-30"
    >
      <div className="relative h-full p-6 flex flex-col">
        <div className="flex justify-between items-start mb-4">
          <div className="h-3 w-3 rounded-full bg-primary"></div>
          {itemData.showVisual && renderVisual(itemData.showVisual)}
        </div>
        <div className="flex-1 flex flex-col justify-between">
          <div>
            {/* Custom styled title */}
            <h2 
              className="text-primary/80 font-medium mb-2"
              style={{
                fontSize: '32px',
                '@media (min-width: 768px)': { fontSize: '48px' }
              }}
            >
              {itemData.text.toUpperCase()}
            </h2>
            
            {/* Custom styled subtitle */}
            <h3 
              className="text-primary font-bold mb-4"
              style={{
                fontSize: '56px',
                lineHeight: '1.1',
                '@media (min-width: 768px)': { fontSize: '72px' }
              }}
            >
              {itemData.subtitle?.toUpperCase()}
            </h3>
          </div>
        </div>
      </div>
    </VerticlesCard>
  );

  return (
    <div className="bg-black flex flex-col items-center justify-center min-h-screen py-8 md:py-16 overflow-hidden">
      <div className="container-responsive">
        <div className="grid gap-4 md:gap-6 grid-cols-1 md:grid-cols-3 auto-rows-min">
        {/* Render all cards */}
        {remainingVerticals.map((itemData, i) => (
          <motion.div
            key={i}
            className={`relative ${getCardClasses(itemData.type)}`}
            style={getCardStyles(itemData.type)} /* Apply proportional sizing */
            custom={i}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: false }}
            variants={cardAnimation}
            whileHover={{ scale: 1.02 }}
          >
            {itemData.text === "E-commerce" ? (
              // Use custom E-commerce card with explicit font sizes
              <EcommerceCard itemData={itemData} />
            ) : (
              // Use regular card for other verticals
              <VerticlesCard
                foldSize={50}
                className={`w-full h-full backdrop-blur-sm border border-primary/20 ${itemData.isSpecial ? 'bg-[#C4D322]' : 'bg-[#D8E35A] bg-opacity-30'}`}
              >
                <div className="relative h-full p-6 flex flex-col">
                  <div className="flex justify-between items-start mb-4">
                    <div className="h-3 w-3 rounded-full bg-primary"></div>
                    {itemData.showVisual && renderVisual(itemData.showVisual)}
                  </div>
                  <div className="flex-1 flex flex-col justify-between">
                    <div>
                      <motion.h2
                        className={`${itemData.isSpecial ? 'text-black' : 'text-primary/80'} text-lg md:text-xl font-medium mb-2`}
                      >
                        {itemData.text.toUpperCase()}
                      </motion.h2>
                      <motion.h3
                        className={`${itemData.isSpecial ? 'text-black' : 'text-primary'} text-2xl md:text-4xl lg:text-5xl font-bold mb-4`}
                      >
                        {itemData.subtitle?.toUpperCase()}
                      </motion.h3>
                    </div>
                    {itemData.isSpecial && (
                      <div className="mt-auto flex flex-col items-start w-full">
                        <button
                          onClick={handleGetStarted}
                          className="mt-2 bg-black text-white px-4 md:px-6 py-2 md:py-3 rounded-md hover:bg-black/80 transition-all duration-300 transform hover:scale-105 touch-target text-sm md:text-base font-medium"
                        >
                          Approach Now
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              </VerticlesCard>
            )}
          </motion.div>
        ))}

        {/* Render the specific row (Pet, Health, Entertainment) at the very bottom */}
        {/* This div will occupy the full width of the grid, ensuring these three cards form their own row */}
        <div className="col-span-full md:col-span-3 grid md:grid-cols-3 gap-6">
          {petIndustryCard && (
            <motion.div
              key="pet-industry"
              className={`relative ${getCardClasses(petIndustryCard.type)}`} // Uses 'medium' type
              custom={10} // Increased delay to appear after others
              initial="hidden"
              whileInView="visible"
              viewport={{ once: false }}
              variants={cardAnimation}
              whileHover={{ scale: 1.02 }}
            >
              <VerticlesCard
                foldSize={50}
                className={`w-full h-full backdrop-blur-sm border border-primary/20 bg-[#D8E35A] bg-opacity-30`}
              >
                <div className="relative h-full p-6 flex flex-col">
                  <div className="flex justify-between items-start mb-4">
                    <div className="h-3 w-3 rounded-full bg-primary"></div>
                    {petIndustryCard.showVisual && renderVisual(petIndustryCard.showVisual)}
                  </div>
                  <div className="flex-1 flex flex-col justify-between">
                    <div>
                      <motion.h2 className={'text-primary/80 text-lg md:text-xl font-medium mb-2'}>
                        {petIndustryCard.text.toUpperCase()}
                      </motion.h2>
                      <motion.h3 className={'text-primary text-2xl md:text-4xl lg:text-5xl font-bold mb-4'}>
                        {petIndustryCard.subtitle?.toUpperCase()}
                      </motion.h3>
                    </div>
                  </div>
                </div>
              </VerticlesCard>
            </motion.div>
          )}
          {healthCard && (
            <motion.div
              key="health-tech"
              className={`relative ${getCardClasses(healthCard.type)}`} // Uses 'medium' type
              custom={11} // Increased delay
              initial="hidden"
              whileInView="visible"
              viewport={{ once: false }}
              variants={cardAnimation}
              whileHover={{ scale: 1.02 }}
            >
              <VerticlesCard
                foldSize={50}
                className={`w-full h-full backdrop-blur-sm border border-primary/20 bg-[#D8E35A] bg-opacity-30`}
              >
                <div className="relative h-full p-6 flex flex-col">
                  <div className="flex justify-between items-start mb-4">
                    <div className="h-3 w-3 rounded-full bg-primary"></div>
                    {healthCard.showVisual && renderVisual(healthCard.showVisual)}
                  </div>
                  <div className="flex-1 flex flex-col justify-between">
                    <div>
                      <motion.h2 className={'text-primary/80 text-lg md:text-xl font-medium mb-2'}>
                        {healthCard.text.toUpperCase()}
                      </motion.h2>
                      <motion.h3 className={'text-primary text-2xl md:text-4xl lg:text-5xl font-bold mb-4'}>
                        {healthCard.subtitle?.toUpperCase()}
                      </motion.h3>
                    </div>
                  </div>
                </div>
              </VerticlesCard>
            </motion.div>
          )}
          {entertainmentCard && (
            <motion.div
              key="entertainment"
              className={`relative ${getCardClasses(entertainmentCard.type)}`} // Uses 'wide' type
              custom={12} // Increased delay
              initial="hidden"
              whileInView="visible"
              viewport={{ once: false }}
              variants={cardAnimation}
              whileHover={{ scale: 1.02 }}
            >
              <VerticlesCard
                foldSize={50}
                className={`w-full h-full backdrop-blur-sm border border-primary/20 bg-[#D8E35A] bg-opacity-30`}
              >
                <div className="relative h-full p-6 flex flex-col">
                  <div className="flex justify-between items-start mb-4">
                    <div className="h-3 w-3 rounded-full bg-primary"></div>
                    {entertainmentCard.showVisual && renderVisual(entertainmentCard.showVisual)}
                  </div>
                  <div className="flex-1 flex flex-col justify-between">
                    <div>
                      <motion.h2 className={'text-primary/80 text-lg md:text-xl font-medium mb-2'}>
                        {entertainmentCard.text.toUpperCase()}
                      </motion.h2>
                      <motion.h3 className={'text-primary text-2xl md:text-4xl lg:text-5xl font-bold mb-4'}>
                        {entertainmentCard.subtitle?.toUpperCase()}
                      </motion.h3>
                    </div>
                  </div>
                </div>
              </VerticlesCard>
            </motion.div>
          )}
        </div>
      </div>
    </div>
    </div>
  );
}


