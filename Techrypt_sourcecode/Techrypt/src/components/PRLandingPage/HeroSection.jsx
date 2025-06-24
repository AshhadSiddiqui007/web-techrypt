import React from 'react';
import '../../pages/LandingPages/PRLandingPage.css';

const HeroSection = () => {
  return (
    <section className="pr-landing-section text-center">
      <div className="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-sm rounded-full px-4 py-2 mb-6 mx-auto">
        <span className="w-2 h-2 pr-landing-dot rounded-full animate-pulse"></span>
        <span className="text-white text-sm">AI-Powered PR Platform</span>
      </div>
      <h1 className="pr-landing-title">
        Transform Your PR<br />
        <span className="pr-landing-title-accent">With AI Intelligence</span>
      </h1>
      <p className="pr-landing-subtitle max-w-4xl mx-auto">
        Revolutionize your public relations strategy with our AI-powered platform.
        Generate compelling press releases, track media coverage, and build meaningful
        relationships with journalists—all in one intelligent suite.
      </p>
      <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-8">
        <button className="pr-landing-btn">Start Free Trial</button>
        <button className="pr-landing-btn" style={{ background: "transparent", color: "#c4d322", border: "1.5px solid #c4d322" }}>
          🎥 Watch Demo
        </button>
      </div>
      <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
        <div className="pr-landing-card">
          <div className="w-16 h-16 bg-[#23281a] rounded-2xl flex items-center justify-center mx-auto mb-6">
            <span className="text-2xl pr-landing-icon">🤖</span>
          </div>
          <h3 className="text-xl font-semibold text-white mb-4">AI Press Release Generator</h3>
          <p className="text-gray-300">Create compelling press releases in minutes with our advanced AI that understands your brand voice and industry trends.</p>
        </div>
        <div className="pr-landing-card">
          <div className="w-16 h-16 bg-[#23281a] rounded-2xl flex items-center justify-center mx-auto mb-6">
            <span className="text-2xl pr-landing-icon">📊</span>
          </div>
          <h3 className="text-xl font-semibold text-white mb-4">Media Intelligence</h3>
          <p className="text-gray-300">Track mentions, analyze sentiment, and measure your PR impact across thousands of media outlets in real-time.</p>
        </div>
        <div className="pr-landing-card">
          <div className="w-16 h-16 bg-[#23281a] rounded-2xl flex items-center justify-center mx-auto mb-6">
            <span className="text-2xl pr-landing-icon">🎯</span>
          </div>
          <h3 className="text-xl font-semibold text-white mb-4">Journalist Network</h3>
          <p className="text-gray-300">Connect with the right journalists using our AI-powered matching system and comprehensive media database.</p>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;