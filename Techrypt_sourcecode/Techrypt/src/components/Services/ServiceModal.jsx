import React from 'react';
import { useNavigate } from 'react-router-dom';
import { serviceDetails } from '../../data/serviceDetails';

const ServiceModal = ({ isOpen, onClose, serviceId }) => {
  const navigate = useNavigate();
  
  if (!isOpen || !serviceId) return null;

  const service = serviceDetails[serviceId];
  if (!service) return null;

  const handleGetConsultation = () => {
    onClose(); // Close the modal first
    // Trigger the chatbot to open with appointment form directly
    const event = new CustomEvent('openTechryptChatbot', {
      detail: {
        contextMessage: "I'd love to help you get started with this service! Let's schedule a consultation to discuss your specific needs.",
        businessType: 'Service Inquiry',
        openAppointmentDirect: true
      }
    });
    window.dispatchEvent(event);
  };

  const handleViewPortfolio = () => {
    onClose(); // Close the modal first
    navigate('/Work'); // Navigate to the Work page (portfolio)
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div className="relative w-full max-w-4xl max-h-[90vh] bg-[#1a1a1a] rounded-2xl border border-[#c4d322] overflow-hidden">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 z-10 w-10 h-10 bg-[#2a2a2a] hover:bg-[#c4d322] rounded-full flex items-center justify-center text-white hover:text-black transition-all duration-300 group"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        {/* Modal Content */}
        <div className="overflow-y-auto max-h-[90vh]">
          {/* Header */}
          <div className="p-8 pb-6 text-center border-b border-[#2a2a2a]">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-3">
              {service.title}
            </h2>
            <p className="text-xl text-[#c4d322] font-semibold mb-4">
              {service.subtitle}
            </p>
            <p className="text-lg text-gray-300 max-w-2xl mx-auto">
              {service.description}
            </p>
          </div>

          {/* Content Grid */}
          <div className="p-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left Column */}
            <div className="space-y-8">
              {/* Benefits */}
              <div>
                <h3 className="text-2xl font-bold text-white mb-4 flex items-center">
                  <span className="w-8 h-8 bg-[#c4d322] rounded-full flex items-center justify-center text-black font-bold mr-3">
                    ✓
                  </span>
                  Why Choose This Service?
                </h3>
                <ul className="space-y-3">
                  {service.benefits.map((benefit, index) => (
                    <li key={index} className="flex items-start text-gray-300">
                      <span className="w-2 h-2 bg-[#c4d322] rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      {benefit}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Process */}
              <div>
                <h3 className="text-2xl font-bold text-white mb-4 flex items-center">
                  <span className="w-8 h-8 bg-[#c4d322] rounded-full flex items-center justify-center text-black font-bold mr-3">
                    →
                  </span>
                  Our Process
                </h3>
                <div className="space-y-3">
                  {service.process.map((step, index) => (
                    <div key={index} className="flex items-start text-gray-300">
                      <span className="w-6 h-6 bg-[#2a2a2a] rounded-full flex items-center justify-center text-[#c4d322] font-bold mr-3 mt-0.5 text-sm">
                        {index + 1}
                      </span>
                      {step}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Right Column */}
            <div className="space-y-8">
              {/* Features */}
              <div>
                <h3 className="text-2xl font-bold text-white mb-4 flex items-center">
                  <span className="w-8 h-8 bg-[#c4d322] rounded-full flex items-center justify-center text-black font-bold mr-3">
                    ⚡
                  </span>
                  What's Included
                </h3>
                <ul className="space-y-3">
                  {service.features.map((feature, index) => (
                    <li key={index} className="flex items-start text-gray-300">
                      <span className="w-2 h-2 bg-[#c4d322] rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Pricing & Timeline */}
              {/* <div className="bg-[#2a2a2a] rounded-xl p-6 border border-[#c4d322]/20">
                <div className="grid grid-cols-2 gap-6 mb-6">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-[#c4d322] mb-1">
                      {service.pricing}
                    </div>
                    <div className="text-gray-400 text-sm">Investment</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-[#c4d322] mb-1">
                      {service.timeline}
                    </div>
                    <div className="text-gray-400 text-sm">Timeline</div>
                  </div>
                </div>
                
                <button 
                  onClick={onClose}
                  className="w-full bg-[#c4d322] text-black font-bold py-4 rounded-lg text-lg transition-all duration-300 hover:bg-[#c4d322]/90 hover:scale-105 shadow-lg hover:shadow-xl"
                >
                  {service.cta}
                </button>
              </div> */}
            </div>
          </div>

          {/* Footer CTA */}
          <div className="p-8 pt-0 text-center border-t border-[#2a2a2a] mt-4">
            <p className="text-gray-400 mb-4">
              Ready to get started? Let's discuss your project and see how we can help.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button 
                onClick={handleGetConsultation}
                className="px-8 py-3 bg-[#c4d322] text-black font-semibold rounded-lg hover:bg-[#c4d322]/90 transition-all duration-300"
              >
                Get Free Consultation
              </button>
              <button 
                onClick={handleViewPortfolio}
                className="px-8 py-3 border-2 border-[#c4d322] text-[#c4d322] font-semibold rounded-lg hover:bg-[#c4d322] hover:text-black transition-all duration-300"
              >
                View Portfolio
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ServiceModal;
