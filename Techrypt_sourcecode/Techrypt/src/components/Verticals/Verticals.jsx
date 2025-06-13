import React, { useState } from "react";
import { motion } from "framer-motion";
import mask1 from "../../assets/svgs/mask1.svg";
import mask2 from "../../assets/svgs/mask2.svg";
import mask3 from "../../assets/svgs/mask3.svg";
import mask4 from "../../assets/svgs/mask4.svg";
import mask5 from "../../assets/svgs/mask5.svg";
import VerticlesCard from "../VerticlesCard/VerticlesCard.jsx";

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
      description: "Learning management systems"
    },
    {
      text: "Fashion",
      class: mask2,
      type: "medium",
      subtitle: "Industry",
      description: "Style and trend platforms"
    },
    {
      text: "Travel",
      class: mask4,
      type: "medium",
      subtitle: "Services",
      description: "Booking and management systems"
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
      type: "medium", // Reverted to original type
      subtitle: "Care",
      description: "Pet care and service platforms"
    },
    {
      text: "Health",
      class: mask3,
      type: "medium", // Reverted to original type
      subtitle: "Tech",
      description: "Healthcare management systems",
      showVisual: "mobile"
    },
    {
      text: "Entertainment",
      class: mask5,
      type: "wide", // Reverted to original type
      subtitle: "Platforms",
      description: "Media and content distribution",
      showVisual: "social"
    },
  ];

  const getCardClasses = (type) => {
    switch(type) {
      case 'large':
        return 'col-span-1 md:col-span-2 row-span-2 min-h-[400px]';
      case 'wide':
        return 'col-span-1 md:col-span-2 min-h-[200px]';
      case 'small':
        return 'col-span-1 md:col-span-1 min-h-[100px] h-[100px]';
      default: // This will catch 'medium' and apply default sizing
        return 'col-span-1 min-h-[200px]';
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

  const EcommerceVisual = () => (
    <div className="absolute top-6 right-6 opacity-30">
      <div className="bg-primary/20 rounded-2xl p-4 w-32 h-24">
        <div className="bg-primary/40 rounded-xl w-full h-16 flex items-center justify-center mb-2">
          <div className="w-8 h-8 bg-primary/60 rounded-lg"></div>
        </div>
      </div>
      <div className="flex space-x-1 mt-2">
        <div className="w-4 h-4 bg-primary/40 rounded"></div>
        <div className="w-4 h-4 bg-primary/50 rounded"></div>
        <div className="w-4 h-4 bg-primary/60 rounded"></div>
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
    <div className="absolute top-6 right-6 opacity-30">
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
      case 'ecommerce': return <EcommerceVisual />;
      case 'chart': return <ChartVisual />;
      case 'mobile': return <MobileVisual />;
      case 'social': return <SocialVisual />;
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

  return (
    <div className="bg-black flex flex-col items-center justify-center min-h-screen pt-10 overflow-hidden">
        <div className="w-11/12 max-w-7xl mx-auto grid gap-6 grid-cols-1 md:grid-cols-3 auto-rows-min px-5 py-4">
            {/* Render all other cards first */}
            {remainingVerticals.map((itemData, i) => (
                <motion.div
                    key={i} // Use original index as they are flowing naturally
                    className={`relative ${getCardClasses(itemData.type)}`}
                    custom={i}
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: false }}
                    variants={cardAnimation}
                    whileHover={{ scale: 1.02 }}
                >
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
                                            className="mt-2 bg-black text-white px-4 py-2 rounded-md hover:bg-black/80 transition-colors align:left"
                                        >
                                            Tell Us Your Industry
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>
                    </VerticlesCard>
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
  );
}


