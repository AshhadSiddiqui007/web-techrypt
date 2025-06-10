import React, { useState, useEffect } from "react";
import "./MessageSidebar.css";
import { BsRobot } from "react-icons/bs";
import TechryptChatbot from "../TechryptChatbot/TechryptChatbot";

const MessageSidebar = () => {
  const [isChatbotOpen, setIsChatbotOpen] = useState(false);
  const [contextualMessage, setContextualMessage] = useState(null);

  const toggleChatbot = () => {
    setIsChatbotOpen(!isChatbotOpen);
  };

  // Listen for custom events to open chatbot with context
  useEffect(() => {
    const handleOpenChatbot = (event) => {
      const { contextMessage, businessType } = event.detail;
      setContextualMessage({ contextMessage, businessType });
      setIsChatbotOpen(true);
    };

    window.addEventListener('openTechryptChatbot', handleOpenChatbot);

    return () => {
      window.removeEventListener('openTechryptChatbot', handleOpenChatbot);
    };
  }, []);

  return (
    <>
      {/* Enhanced Chatbot Trigger Button with Techrypt Brand Color */}
      <BsRobot
        title="Techrypt AI Assistant - ChatGPT-like Intelligence"
        className="fixed bottom-8 right-8 z-[999] text-white text-5xl rounded-full p-3 hover:scale-110 duration-300 transition-all cursor-pointer shadow-lg hover:shadow-xl"
        style={{
          background: 'linear-gradient(135deg, #AEBB1E 0%, #D3DC5A 100%)',
          boxShadow: '0 8px 32px rgba(174, 187, 30, 0.3)'
        }}
        onMouseEnter={(e) => {
          e.target.style.background = 'linear-gradient(135deg, #D3DC5A 0%, #AEBB1E 100%)';
          e.target.style.boxShadow = '0 12px 40px rgba(174, 187, 30, 0.5)';
        }}
        onMouseLeave={(e) => {
          e.target.style.background = 'linear-gradient(135deg, #AEBB1E 0%, #D3DC5A 100%)';
          e.target.style.boxShadow = '0 8px 32px rgba(174, 187, 30, 0.3)';
        }}
        onClick={toggleChatbot}
      />

      {/* Enhanced TechryptChatbot with Smart Features */}
      {isChatbotOpen && (
        <TechryptChatbot
          isOpen={isChatbotOpen}
          onClose={() => {
            setIsChatbotOpen(false);
            setContextualMessage(null);
          }}
          contextualMessage={contextualMessage}
        />
      )}
    </>
  );
};

export default MessageSidebar;
