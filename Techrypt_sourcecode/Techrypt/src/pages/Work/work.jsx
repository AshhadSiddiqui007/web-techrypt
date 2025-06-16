import React from "react";
import Hero from "../../components/Hero/Hero";
import OtherWorks from "../../components/OtherWorks/OtherWorks";
import Filter from "../../components/Filter/Filter.jsx"; // Added .jsx extension for explicit resolution

const work = () => {
  // Function to open the chatbot (reusing the CustomEvent pattern)
  const handleOpenChatbot = () => {
    const event = new CustomEvent('openTechryptChatbot', {
      detail: {
        contextMessage: "I'm interested in becoming a potential client. How can I get started?",
        businessType: 'Potential Client Inquiry'
      }
    });
    window.dispatchEvent(event);
  };

  return (
    <div style={{ backgroundColor: "#0f0f0f" }} className="min-h-screen">
      <div className="container-responsive spacing-responsive-lg text-center">
        <h1 className="text-responsive-4xl md:text-6xl lg:text-7xl font-black text-white mb-8 md:mb-16 uppercase tracking-wider relative animate-fade-in">
          Our Work
          <span className="absolute -bottom-4 left-1/2 transform -translate-x-1/2 w-32 md:w-48 lg:w-64 h-1.5 bg-primary block animate-underline-grow"></span>
        </h1>
        <style>
          {`
            @keyframes fadeIn {
              0% { opacity: 0; transform: translateY(20px); }
              100% { opacity: 1; transform: translateY(0); }
            }
            @keyframes underlineGrow {
              0% { width: 0; }
              100% { width: 100%; }
            }
            .animate-fade-in {
              animation: fadeIn 1.5s ease-in-out;
            }
            .animate-underline-grow {
              animation: underlineGrow 1.5s ease-in-out;
            }
          `}
        </style>
      </div>

      {/* Enhanced Mobile-Responsive Client Section */}
      <div className="flex flex-col md:flex-row items-center justify-center gap-6 md:gap-8 lg:gap-12 py-8 md:py-12 px-4 md:px-8 bg-[#0f0f0f] border-b border-white/10 mb-8 md:mb-12">
        <h2 className="text-responsive-2xl md:text-responsive-3xl lg:text-4xl font-semibold text-white text-center md:text-left max-w-sm md:max-w-md lg:max-w-lg leading-tight">
          Interested in being a potential client?
        </h2>

        {/* Vertical line - hidden on mobile, visible on desktop */}
        <div className="hidden md:block w-0.5 h-24 lg:h-32 bg-white rounded-full shadow-lg"></div>

        {/* Horizontal line - visible on mobile, hidden on desktop */}
        <div className="block md:hidden w-24 h-0.5 bg-white rounded-full shadow-lg"></div>

        <button
          onClick={handleOpenChatbot}
          className="bg-primary hover:bg-primary/80 text-black font-bold py-3 md:py-4 px-6 md:px-8 lg:px-10 rounded-full text-responsive-base md:text-responsive-lg transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl touch-target"
        >
          Talk To Our Expert
        </button>
      </div>

      <Filter />
    </div>
  );
};

export default work;
