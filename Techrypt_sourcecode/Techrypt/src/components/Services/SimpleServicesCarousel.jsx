import React from 'react';

const SimpleServicesCarousel = () => {
  const services = [
    'SEO',
    'DIGITAL MARKETING',
    'WEB DESIGN',
    'UI / UX',
    'APP DESIGN'
  ];

  return (
    <div className="w-full py-6 overflow-hidden" style={{ backgroundColor: '#2d2d2d' }}>
      <div className="flex animate-scroll whitespace-nowrap items-center">
        {[...Array(2)].map((_, repeatIdx) =>
          services.map((service, index) => (
            <React.Fragment key={service + repeatIdx}>
              <span className="px-12 font-medium text-2xl tracking-widest text-white flex items-center justify-center">
                {service}
              </span>
              {/* Add spacer after every item except the very last one */}
              {!(repeatIdx === 1 && index === services.length - 1) && (
                <span className="mx-4 text-2xl" style={{ color: '#c4d322' }}>✦</span>
              )}
            </React.Fragment>
          ))
        )}
      </div>
      <style jsx>{`
        @keyframes scroll {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
        .animate-scroll {
          animation: scroll 20s linear infinite;
        }
        .animate-scroll:hover {
          animation-play-state: paused;
        }
      `}</style>
    </div>
  );
};

export default SimpleServicesCarousel;
