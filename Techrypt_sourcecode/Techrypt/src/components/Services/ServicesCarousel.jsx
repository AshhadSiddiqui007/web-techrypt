import React, { useState, useEffect } from 'react';
import { FiChevronLeft, FiChevronRight, FiCode, FiSearch, FiTrendingUp, FiSmartphone, FiLayers, FiUsers } from 'react-icons/fi';

const ServicesCarousel = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isAutoPlay, setIsAutoPlay] = useState(true);

  const services = [
    {
      id: 1,
      title: "Web Development",
      description: "Custom websites built with modern technologies, optimized for performance and user experience.",
      icon: <FiCode className="w-8 h-8" />,
      features: ["Responsive Design", "Fast Loading", "SEO Optimized", "Mobile First"],
      color: "from-blue-500 to-cyan-500"
    },
    {
      id: 2,
      title: "SEO Optimization",
      description: "Boost your search engine rankings with our comprehensive SEO strategies and technical optimization.",
      icon: <FiSearch className="w-8 h-8" />,
      features: ["Keyword Research", "Technical SEO", "Content Strategy", "Analytics"],
      color: "from-green-500 to-emerald-500"
    },
    {
      id: 3,
      title: "Digital Marketing",
      description: "Drive growth with data-driven marketing campaigns across all digital channels.",
      icon: <FiTrendingUp className="w-8 h-8" />,
      features: ["Social Media", "PPC Campaigns", "Email Marketing", "Content Creation"],
      color: "from-purple-500 to-pink-500"
    },
    {
      id: 4,
      title: "Mobile App Design",
      description: "Create engaging mobile experiences with intuitive design and seamless functionality.",
      icon: <FiSmartphone className="w-8 h-8" />,
      features: ["iOS & Android", "UI/UX Design", "Prototyping", "User Testing"],
      color: "from-orange-500 to-red-500"
    },
    {
      id: 5,
      title: "UI/UX Design",
      description: "Design beautiful, user-centered interfaces that convert visitors into customers.",
      icon: <FiLayers className="w-8 h-8" />,
      features: ["User Research", "Wireframing", "Visual Design", "Usability Testing"],
      color: "from-indigo-500 to-purple-500"
    },
    {
      id: 6,
      title: "Brand Strategy",
      description: "Build a strong brand identity that resonates with your target audience and drives loyalty.",
      icon: <FiUsers className="w-8 h-8" />,
      features: ["Brand Identity", "Logo Design", "Brand Guidelines", "Market Research"],
      color: "from-teal-500 to-green-500"
    }
  ];

  // Auto-play functionality
  useEffect(() => {
    if (!isAutoPlay) return;
    
    const interval = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % services.length);
    }, 4000);

    return () => clearInterval(interval);
  }, [isAutoPlay, services.length]);

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % services.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + services.length) % services.length);
  };

  const goToSlide = (index) => {
    setCurrentSlide(index);
  };

  return (
    <div className="relative w-full max-w-6xl mx-auto px-4">
      {/* Header */}
      <div className="text-center mb-12">
        <p className="text-gray-400 text-lg max-w-2xl mx-auto">
          We offer comprehensive digital solutions to help your business thrive in the modern world
        </p>
      </div>

      {/* Carousel Container */}
      <div 
        className="relative bg-[#1a1a1a] rounded-2xl overflow-hidden shadow-2xl"
        onMouseEnter={() => setIsAutoPlay(false)}
        onMouseLeave={() => setIsAutoPlay(true)}
      >
        {/* Main Carousel */}
        <div className="relative h-[500px] md:h-[400px]">
          {services.map((service, index) => (
            <div
              key={service.id}
              className={`absolute inset-0 transition-all duration-700 ease-in-out ${
                index === currentSlide
                  ? 'opacity-100 translate-x-0'
                  : index < currentSlide
                  ? 'opacity-0 -translate-x-full'
                  : 'opacity-0 translate-x-full'
              }`}
            >
              <div className="flex flex-col md:flex-row h-full">
                {/* Content Side */}
                <div className="flex-1 p-8 md:p-12 flex flex-col justify-center">
                  <div className={`inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-r ${service.color} mb-6`}>
                    <div className="text-white">
                      {service.icon}
                    </div>
                  </div>
                  
                  <h3 className="text-3xl md:text-4xl font-bold text-white mb-4">
                    {service.title}
                  </h3>
                  
                  <p className="text-gray-300 text-lg mb-6 leading-relaxed">
                    {service.description}
                  </p>
                  
                  <div className="grid grid-cols-2 gap-3 mb-8">
                    {service.features.map((feature, idx) => (
                      <div key={idx} className="flex items-center">
                        <div className={`w-2 h-2 rounded-full bg-gradient-to-r ${service.color} mr-3`} />
                        <span className="text-gray-400 text-sm">{feature}</span>
                      </div>
                    ))}
                  </div>
                  
                  <button className={`inline-flex items-center px-6 py-3 bg-gradient-to-r ${service.color} text-white font-semibold rounded-lg hover:shadow-lg transition-all duration-300 transform hover:scale-105 w-fit`}>
                    Learn More
                    <FiChevronRight className="ml-2 w-4 h-4" />
                  </button>
                </div>

                {/* Visual Side */}
                <div className="flex-1 relative overflow-hidden">
                  <div className={`absolute inset-0 bg-gradient-to-br ${service.color} opacity-10`} />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className={`w-48 h-48 rounded-full bg-gradient-to-r ${service.color} opacity-20 animate-pulse`} />
                  </div>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className={`text-8xl opacity-30 bg-gradient-to-r ${service.color} bg-clip-text text-transparent`}>
                      {service.icon}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Navigation Arrows */}
        <button
          onClick={prevSlide}
          className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-3 rounded-full transition-all duration-300 backdrop-blur-sm"
        >
          <FiChevronLeft className="w-6 h-6" />
        </button>
        
        <button
          onClick={nextSlide}
          className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-3 rounded-full transition-all duration-300 backdrop-blur-sm"
        >
          <FiChevronRight className="w-6 h-6" />
        </button>

        {/* Progress Bar */}
        <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
          {services.map((_, index) => (
            <button
              key={index}
              onClick={() => goToSlide(index)}
              className={`w-3 h-3 rounded-full transition-all duration-300 ${
                index === currentSlide
                  ? 'bg-primary scale-125'
                  : 'bg-gray-600 hover:bg-gray-400'
              }`}
            />
          ))}
        </div>

        {/* Service Counter */}
        <div className="absolute top-4 right-4 bg-black/50 text-white px-3 py-1 rounded-full text-sm backdrop-blur-sm">
          {currentSlide + 1} / {services.length}
        </div>
      </div>

      {/* Service Thumbnails */}
      <div className="flex justify-center mt-8 space-x-4 overflow-x-auto pb-4">
        {services.map((service, index) => (
          <button
            key={service.id}
            onClick={() => goToSlide(index)}
            className={`flex-shrink-0 p-4 rounded-xl transition-all duration-300 ${
              index === currentSlide
                ? 'bg-primary/20 border-2 border-primary'
                : 'bg-gray-800 hover:bg-gray-700 border-2 border-transparent'
            }`}
          >
            <div className={`w-8 h-8 mx-auto mb-2 text-${index === currentSlide ? 'primary' : 'gray-400'}`}>
              {service.icon}
            </div>
            <span className={`text-xs font-medium ${
              index === currentSlide ? 'text-primary' : 'text-gray-400'
            }`}>
              {service.title.split(' ')[0]}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default ServicesCarousel;
