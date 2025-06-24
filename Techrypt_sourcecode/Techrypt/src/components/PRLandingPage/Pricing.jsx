import React from 'react';
import '../../pages/LandingPages/PRLandingPage.css';

const Pricing = () => {
  return (
    <section className="pr-landing-section">
      <div className="text-center mb-8">
        <h2 className="pr-landing-title">Choose Your <span className="pr-landing-title-accent">Plan</span></h2>
        <p className="pr-landing-subtitle max-w-3xl mx-auto">
          Flexible pricing options to fit your PR needs, from startups to enterprise organizations.
        </p>
      </div>
      <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
        <div className="pr-landing-pricing">
          <h3 className="text-2xl font-bold text-white mb-2">Starter</h3>
          <div className="price">$49<span className="text-lg text-gray-400">/month</span></div>
          <ul className="space-y-3 mb-8">
            <li className="flex items-center text-gray-300"><span className="pr-landing-check mr-2">✓</span>5 Press Releases/month</li>
            <li className="flex items-center text-gray-300"><span className="pr-landing-check mr-2">✓</span>Basic Analytics</li>
            <li className="flex items-center text-gray-300"><span className="pr-landing-check mr-2">✓</span>Email Support</li>
          </ul>
          <button className="pr-landing-btn w-full">Get Started</button>
        </div>
        <div className="pr-landing-pricing" style={{ border: "2px solid #c4d322" }}>
          <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 bg-[#c4d322] text-[#121212] px-4 py-1 rounded-full text-sm font-bold" style={{ position: "absolute", top: "-1.5rem", left: "50%", transform: "translateX(-50%)" }}>
            Most Popular
          </div>
          <h3 className="text-2xl font-bold text-white mb-2">Professional</h3>
          <div className="price">$149<span className="text-lg text-gray-400">/month</span></div>
          <ul className="space-y-3 mb-8">
            <li className="flex items-center text-gray-300"><span className="pr-landing-check mr-2">✓</span>25 Press Releases/month</li>
            <li className="flex items-center text-gray-300"><span className="pr-landing-check mr-2">✓</span>Advanced Analytics</li>
            <li className="flex items-center text-gray-300"><span className="pr-landing-check mr-2">✓</span>Media Database Access</li>
            <li className="flex items-center text-gray-300"><span className="pr-landing-check mr-2">✓</span>Priority Support</li>
          </ul>
          <button className="pr-landing-btn w-full">Get Started</button>
        </div>
        <div className="pr-landing-pricing">
          <h3 className="text-2xl font-bold text-white mb-2">Enterprise</h3>
          <div className="price">Custom</div>
          <ul className="space-y-3 mb-8">
            <li className="flex items-center text-gray-300"><span className="pr-landing-check mr-2">✓</span>Unlimited Press Releases</li>
            <li className="flex items-center text-gray-300"><span className="pr-landing-check mr-2">✓</span>Custom Integrations</li>
            <li className="flex items-center text-gray-300"><span className="pr-landing-check mr-2">✓</span>Dedicated Account Manager</li>
            <li className="flex items-center text-gray-300"><span className="pr-landing-check mr-2">✓</span>24/7 Support</li>
          </ul>
          <button className="pr-landing-btn w-full">Contact Sales</button>
        </div>
      </div>
    </section>
  );
};

export default Pricing;