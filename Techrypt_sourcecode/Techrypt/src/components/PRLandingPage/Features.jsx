import React from 'react';
import '../../pages/LandingPages/PRLandingPage.css';

const Features = () => {
  return (
    <section className="pr-landing-section">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h2 className="pr-landing-title">Powerful Features for <span className="pr-landing-title-accent">Modern PR</span></h2>
          <p className="pr-landing-subtitle max-w-3xl mx-auto">
            Everything you need to execute successful PR campaigns, powered by cutting-edge AI technology.
          </p>
        </div>
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8">
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 bg-[#23281a] rounded-xl flex items-center justify-center flex-shrink-0">
                <span className="text-xl pr-landing-icon">✨</span>
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white mb-2">Smart Content Creation</h3>
                <p className="text-gray-300">Generate press releases, pitches, and media kits that resonate with your target audience using advanced AI algorithms.</p>
              </div>
            </div>
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 bg-[#23281a] rounded-xl flex items-center justify-center flex-shrink-0">
                <span className="text-xl pr-landing-icon">📈</span>
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white mb-2">Real-time Analytics</h3>
                <p className="text-gray-300">Monitor your PR performance with comprehensive analytics, sentiment analysis, and ROI tracking.</p>
              </div>
            </div>
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 bg-[#23281a] rounded-xl flex items-center justify-center flex-shrink-0">
                <span className="text-xl pr-landing-icon">🔗</span>
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white mb-2">Media Relationship Management</h3>
                <p className="text-gray-300">Build and maintain relationships with journalists, influencers, and media outlets through our integrated CRM.</p>
              </div>
            </div>
          </div>
          <div className="pr-landing-card">
            <h4 className="text-lg font-semibold text-white mb-2">AI-Powered Dashboard</h4>
            <p className="text-gray-300">Get insights at a glance with our intelligent dashboard that learns from your PR activities.</p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Features;