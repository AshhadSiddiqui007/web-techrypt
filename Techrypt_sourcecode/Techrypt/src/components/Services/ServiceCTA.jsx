import React, { useState } from 'react';

const ServiceCTA = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    service: '',
    message: ''
  });

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission here
    console.log('Form submitted:', formData);
    setIsModalOpen(false);
    // Reset form
    setFormData({
      name: '',
      email: '',
      service: '',
      message: ''
    });
  };

  return (
    <>
      <section className="relative py-20 px-4 overflow-hidden" style={{ background: 'linear-gradient(to bottom, rgba(196, 211, 34, 0.05) 0%, rgba(196, 211, 34, 0.08) 20%, #000000 60%, #000000 100%)' }}>
        {/* Background Effects */}
        <div className="absolute inset-0">
          <div className="absolute top-0 left-1/4 w-96 h-96 rounded-full blur-3xl animate-pulse" style={{ backgroundColor: 'rgba(196, 211, 34, 0.1)' }}></div>
          <div className="absolute bottom-0 right-1/4 w-96 h-96 rounded-full blur-3xl animate-pulse" style={{ backgroundColor: 'rgba(196, 211, 34, 0.15)', animationDelay: '1s' }}></div>
        </div>

        <div className="relative z-10 max-w-4xl mx-auto text-center">
          {/* Heading */}
          <h2 className="text-4xl md:text-6xl font-bold text-white mb-6">
            Ready to Elevate Your Business?
          </h2>
          
          {/* Subheading */}
          <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-2xl mx-auto">
            Let's build something extraordinary together. Transform your vision into reality with our cutting-edge solutions.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
            <button
              onClick={() => setIsModalOpen(true)}
              className="group relative px-8 py-4 md:px-12 md:py-6 text-white font-bold text-lg md:text-xl rounded-full transition-all duration-300 hover:scale-105 hover:shadow-2xl transform"
              style={{ 
                backgroundColor: '#c4d322',
                boxShadow: isModalOpen ? 'none' : '0 25px 50px -12px rgba(196, 211, 34, 0.25)'
              }}
            >
              <span className="relative z-10">Get Started</span>
            </button>
            
            <button className="group px-8 py-4 md:px-12 md:py-6 border-2 border-white text-white hover:bg-white hover:text-black font-bold text-lg md:text-xl rounded-full transition-all duration-300 hover:scale-105">
              View Our Work
              <svg className="inline-block ml-2 w-5 h-5 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </button>
          </div>

          {/* Stats */}
          <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8">
            {[
              { number: '500+', label: 'Projects Completed' },
              { number: '250+', label: 'Happy Clients' },
              { number: '50+', label: 'Team Members' },
              { number: '5+', label: 'Years Experience' }
            ].map((stat, index) => (
              <div key={index} className="text-center group">
                <div className="text-3xl md:text-4xl font-bold text-white mb-2 transition-colors" style={{ color: stat.isHovered ? '#c4d322' : 'white' }}>
                  {stat.number}
                </div>
                <div className="text-gray-400 group-hover:text-gray-300 transition-colors">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
          <div className="relative w-full max-w-md bg-gray-900 rounded-2xl p-8 border border-gray-700">
            {/* Close Button */}
            <button
              onClick={() => setIsModalOpen(false)}
              className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="text-center mb-8">
                <h3 className="text-2xl font-bold text-white mb-2">Get Started</h3>
                <p className="text-gray-400">Tell us about your project</p>
              </div>

              <div>
                <input
                  type="text"
                  name="name"
                  placeholder="Your Name"
                  value={formData.name}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:border-transparent"
                  style={{ focusRingColor: '#c4d322' }}
                  onFocus={(e) => e.target.style.borderColor = '#c4d322'}
                  onBlur={(e) => e.target.style.borderColor = '#374151'}
                  required
                />
              </div>

              <div>
                <input
                  type="email"
                  name="email"
                  placeholder="Your Email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:border-transparent"
                  style={{ focusRingColor: '#c4d322' }}
                  onFocus={(e) => e.target.style.borderColor = '#c4d322'}
                  onBlur={(e) => e.target.style.borderColor = '#374151'}
                  required
                />
              </div>

              <div>
                <select
                  name="service"
                  value={formData.service}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:border-transparent"
                  style={{ focusRingColor: '#c4d322' }}
                  onFocus={(e) => e.target.style.borderColor = '#c4d322'}
                  onBlur={(e) => e.target.style.borderColor = '#374151'}
                  required
                >
                  <option value="">Select a Service</option>
                  <option value="branding">Branding & Logo Design</option>
                  <option value="digital-marketing">Digital Marketing</option>
                  <option value="web-development">Web Development</option>
                  <option value="ai-chatbots">AI & Chatbots</option>
                  <option value="software-development">Software Development</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div>
                <textarea
                  name="message"
                  placeholder="Tell us about your project..."
                  value={formData.message}
                  onChange={handleInputChange}
                  rows={4}
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:border-transparent resize-none"
                  style={{ focusRingColor: '#c4d322' }}
                  onFocus={(e) => e.target.style.borderColor = '#c4d322'}
                  onBlur={(e) => e.target.style.borderColor = '#374151'}
                  required
                ></textarea>
              </div>

              <button
                type="submit"
                className="w-full py-3 text-white font-bold rounded-lg transition-all duration-300 hover:shadow-lg transform hover:scale-105"
                style={{ backgroundColor: '#c4d322' }}
              >
                Send Message
              </button>
            </form>
          </div>
        </div>
      )}
    </>
  );
};

export default ServiceCTA;
