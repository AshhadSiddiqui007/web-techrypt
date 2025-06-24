import React from 'react';

const CTA = ({ onGetStarted }) => {
  return (
    <section className="pr-landing-section text-center">
      <h2 className="pr-landing-title">
        Ready to <span className="pr-landing-title-accent">Transform Your PR?</span>
      </h2>
      <p className="pr-landing-subtitle max-w-2xl mx-auto">
        Join thousands of PR professionals who are already using TechyPR to create more impactful campaigns.
      </p>
      <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
        <button className="pr-landing-btn">Start Your Free Trial</button>
        <button className="pr-landing-btn" 
        onClick={onGetStarted} 
        style={{ background: "transparent", color: "#c4d322", border: "1.5px solid #c4d322" }}>
          <span>💬 Chat with our AI assistant</span>
        </button>
      </div>
    </section>
  );
};

export default CTA;


