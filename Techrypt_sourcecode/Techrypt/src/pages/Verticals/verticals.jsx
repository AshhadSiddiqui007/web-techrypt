import React from "react";
import Hero from "../../components/Hero/Hero.jsx";
import Verticals from "../../components/Verticals/Verticals.jsx";

const VerticalsPage = () => {
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
    <div style={{ backgroundColor: "#0f0f0f" }}>
      <div
        style={{
          padding: "40px",
          textAlign: "center",
        }}
      >
        <h1
          className="text-3xl sm:text-4xl md:text-6xl font-extrabold uppercase tracking-wider relative"
          style={{
            color: "#ffffff",
            marginBottom: "60px",
            position: "relative",
            animation: "fadeIn 1.5s ease-in-out",
          }}
        >
          Our Verticals
          <span
            style={{
              color: "#a3d900",
              position: "absolute",
              bottom: "-15px",
              left: "50%",
              transform: "translateX(-50%)",
              width: "250px",
              height: "6px",
              background: "#a3d900",
              display: "block",
              animation: "underlineGrow 1.5s ease-in-out",
            }}
          ></span>
        </h1>
        <style>
          {`
            @keyframes fadeIn {
              0% { opacity: 0; transform: translateY(20px); }
              100% { opacity: 1; transform: translateY(0); }
            }
            @keyframes underlineGrow {
              0% { width: 0; }
              100% { width: 250px; }
            }
          `}
        </style>
      </div>
      <Verticals />
    </div>
  );
};

export default VerticalsPage;
