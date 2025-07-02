import React, { useState } from 'react';

const ServiceCard = ({ service, index, isVisible, onLearnMore }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      className={`group relative rounded-2xl p-8 transition-all duration-500 hover:-translate-y-2 hover:shadow-2xl ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
      }`}
      style={{
        backgroundColor: '#1a1a1a',
        transitionDelay: `${index * 100}ms`,
        boxShadow: isHovered ? '0 25px 50px -12px rgba(196, 211, 34, 0.25)' : 'none'
      }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Background Gradient Overlay */}
      <div className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" style={{ background: 'linear-gradient(135deg, rgba(196, 211, 34, 0.05), rgba(255, 255, 255, 0.02))' }}></div>
      
      {/* Content */}
      <div className="relative z-10">
        {/* Icon */}
        <div className="text-5xl mb-6 transform group-hover:scale-110 transition-transform duration-300">
          {service.icon}
        </div>

        {/* Title */}
        <h3 className="text-2xl font-bold text-white mb-4 transition-colors duration-300" style={{ color: isHovered ? '#c4d322' : 'white' }}>
          {service.title}
        </h3>

        {/* Description */}
        <p className="text-gray-400 mb-6 leading-relaxed">
          {service.description}
        </p>

        {/* Features */}
        <div className="mb-6">
          <div className="flex flex-wrap gap-2">
            {service.features.map((feature, featureIndex) => (
              <span
                key={featureIndex}
                className="px-3 py-1 text-sm rounded-full border transition-all duration-300"
                style={{
                  backgroundColor: '#2a2a2a',
                  borderColor: isHovered ? '#c4d322' : '#444444',
                  color: isHovered ? '#c4d322' : '#cccccc'
                }}
              >
                {feature}
              </span>
            ))}
          </div>
        </div>

        {/* CTA Button */}
        <div className={`transition-all duration-300 ${isHovered ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
          <button 
            onClick={() => onLearnMore(service.id)}
            className="w-full py-3 text-white font-semibold rounded-lg transition-all duration-300 hover:shadow-lg transform hover:scale-105"
            style={{ backgroundColor: '#c4d322' }}
          >
            Learn More
          </button>
        </div>

        {/* Hover Arrow */}
        <div className={`absolute top-6 right-6 transition-all duration-300 ${isHovered ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-4'}`}>
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" style={{ color: '#c4d322' }}>
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </div>
      </div>
    </div>
  );
};

export default ServiceCard;
