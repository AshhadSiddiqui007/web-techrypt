import React from 'react';
import { FiMonitor, FiSmartphone, FiGlobe, FiShield, FiUsers, FiTrendingUp, FiSettings, FiHeart } from 'react-icons/fi';

const SimpleServicesCarousel = () => {
  const services = [
    { name: 'Web Development', icon: FiGlobe },
    { name: 'Mobile Apps', icon: FiSmartphone },
    { name: 'UI/UX Design', icon: FiMonitor },
    { name: 'Cybersecurity', icon: FiShield },
    { name: 'Digital Marketing', icon: FiTrendingUp },
    { name: 'Consulting', icon: FiUsers },
    { name: 'System Integration', icon: FiSettings },
    { name: 'Support & Maintenance', icon: FiHeart },
  ];

  return (
    <div className="w-full bg-grey-400 py-4 overflow-hidden">
      <div className="flex animate-scroll whitespace-nowrap">
        {/* First set of services */}
        {services.map((service, index) => {
          const IconComponent = service.icon;
          return (
            <div key={index} className="flex items-center mx-6">
              <IconComponent className="text-lg mr-2" style={{ color: '#c4d322' }} />
              <span className="font-medium text-sm" style={{ color: '#c4d322' }}>
                {service.name}
              </span>
              {index < services.length - 1 && (
                <span className="text-gray-400 mx-12">•</span>
              )}
            </div>
          );
        })}
        
        {/* Duplicate set for seamless scrolling */}
        {services.map((service, index) => {
          const IconComponent = service.icon;
          return (
            <div key={`duplicate-${index}`} className="flex items-center mx-6">
              <IconComponent className="text-lg mr-2" style={{ color: '#c4d322' }} />
              <span className="font-medium text-sm" style={{ color: '#c4d322' }}>
                {service.name}
              </span>
              {index < services.length - 1 && (
                <span className="text-gray-400 mx-6">•</span>
              )}
            </div>
          );
        })}
      </div>

      <style jsx>{`
        @keyframes scroll {
          0% {
            transform: translateX(0);
          }
          100% {
            transform: translateX(-50%);
          }
        }
        
        .animate-scroll {
          animation: scroll 30s linear infinite;
        }
        
        .animate-scroll:hover {
          animation-play-state: paused;
        }
      `}</style>
    </div>
  );
};

export default SimpleServicesCarousel;
