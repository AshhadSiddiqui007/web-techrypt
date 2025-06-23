import React from "react";
import './PRLandinngPage.css';

const PRLandingPage = () => (
  <div className="pr-landing-root">
    <div className="pr-broadcast-anim">
  <span className="pr-broadcast-center"></span>
  <span className="pr-broadcast-wave wave1"></span>
  <span className="pr-broadcast-wave wave2"></span>
</div>
    <div className="pr-broadcast-creative">
  <div className="pr-megaphone">
    <div className="pr-megaphone-mouth"></div>
    <div className="pr-megaphone-handle"></div>
  </div>
  <span className="pr-broadcast-wave-creative"></span>
  <span className="pr-broadcast-wave-creative wave2"></span>
  <span className="pr-broadcast-wave-creative wave3"></span>
</div>
    {/* Hero Section */}
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
      {/* Feature Cards */}
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

    {/* Features Section */}
    <section className="pr-landing-section">
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
    </section>

    {/* Pricing Section */}
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

    {/* CTA Section */}
    <section className="pr-landing-section text-center">
      <h2 className="pr-landing-title">
        Ready to <span className="pr-landing-title-accent">Transform Your PR?</span>
      </h2>
      <p className="pr-landing-subtitle max-w-2xl mx-auto">
        Join thousands of PR professionals who are already using TechyPR to create more impactful campaigns.
      </p>
      <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
        <button className="pr-landing-btn">Start Your Free Trial</button>
        <button className="pr-landing-btn" style={{ background: "transparent", color: "#c4d322", border: "1.5px solid #c4d322" }}>
          <span>💬 Chat with our AI assistant</span>
        </button>
      </div>
    </section>
    <div className="pr-talking-anim">
  <div className="pr-talking-person">
    <span className="pr-talking-bubble">Let’s connect!</span>
  </div>
  <div className="pr-talking-person green">
    <span className="pr-talking-bubble">Excited to share news!</span>
  </div>
  <div className="pr-talking-person">
    <span className="pr-talking-bubble">Ready for your story?</span>
  </div>
</div>
  </div>
);

export default PRLandingPage;
