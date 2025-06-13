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
    <div style={{ backgroundColor: "#0f0f0f" }}>
      <div
        style={{
          padding: "60px 20px",
          textAlign: "center",
        }}
      >
        <h1
          style={{
            fontSize: "64px",
            fontWeight: "900",
            color: "#ffffff",
            marginBottom: "60px",
            textTransform: "uppercase",
            letterSpacing: "3px",
            position: "relative",
            animation: "fadeIn 1.5s ease-in-out",
          }}
        >

          Our Work
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

      {/* NEW SECTION: Interested in being a client? */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center', // Keep content centered within the page
          gap: '30px', /* Space between text, line, and button */
          padding: '40px 20px',
          backgroundColor: '#0f0f0f', /* Match page background */
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)', /* Subtle separator */
          marginBottom: '40px', /* Space before Filter component */
          flexWrap: 'wrap', /* Allow wrapping on small screens */
        }}
      >
        <h2
          style={{
            fontSize: '2.5rem', /* Large text size */
            fontWeight: '600',
            color: '#ffffff',
            textAlign: 'left', /* CHANGED: Text alignment to left */
            flexBasis: 'auto', /* Allow text to size naturally */
            maxWidth: '350px', /* Prevent text from being too wide */
            lineHeight: '1.2',
            textShadow: '0 0 10px rgba(255, 255, 255, 0.1)'
          }}
        >
          Interested in being a potential client?
        </h2>
        <div
          style={{
            width: '2px',
            height: '150px', /* Height of the vertical line */
            backgroundColor: '#ffffff',
            borderRadius: '1px',
            boxShadow: '0 0 5px rgba(255, 255, 255, 0.5)', /* Subtle glow */
            flexShrink: 0, /* Prevent shrinking on smaller screens */
          }}
        ></div>
        <button
          onClick={handleOpenChatbot}
          style={{
            backgroundColor: '#C4D322', /* CHANGED: Button background color */
            color: '#0f0f0f', /* Black text for contrast */
            padding: '20px 40px',
            borderRadius: '50px', /* Rounded button */
            fontSize: '1.2rem',
            fontWeight: 'bold',
            border: 'none',
            cursor: 'pointer',
            transition: 'background-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease',
            boxShadow: '0 5px 15px rgba(196, 211, 34, 0.3)', /* UPDATED: Initial subtle shadow */
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = 'rgba(196, 211, 34, 0.8)'; /* UPDATED: Darker color on hover */
            e.currentTarget.style.transform = 'scale(1.05)';
            e.currentTarget.style.boxShadow = '0 8px 20px rgba(196, 211, 34, 0.5)'; /* UPDATED: Hover shadow */
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = '#C4D322'; /* UPDATED: Back to original color on leave */
            e.currentTarget.style.transform = 'scale(1)';
            e.currentTarget.style.boxShadow = '0 5px 15px rgba(196, 211, 34, 0.3)'; /* UPDATED: Back to original shadow on leave */
          }}
        >
          Open Chatbot
        </button>
      </div>

      {/* Existing Filter component */}
      <Filter />
    </div>
  );
};

export default work;
