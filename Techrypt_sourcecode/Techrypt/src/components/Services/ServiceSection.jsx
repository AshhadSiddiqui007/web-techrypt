import React, { useState, useEffect } from 'react';
import ServiceCard from './ServiceCard';
import ServiceModal from './ServiceModal';

const ServiceSection = () => {
  const [activeCategory, setActiveCategory] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [visibleCards, setVisibleCards] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedServiceId, setSelectedServiceId] = useState(null);

  const handleLearnMore = (serviceId) => {
    setSelectedServiceId(serviceId);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedServiceId(null);
  };

  const categories = [
    { id: 'all', name: 'All Services' },
    { id: 'digital', name: 'Digital Agency' },
    { id: 'premium', name: 'Premium Services' },
    { id: 'software', name: 'Software Development' }
  ];

  const services = [
    // Digital Agency
    {
      id: 1,
      category: 'digital',
      title: 'Branding & Logo Design',
      description: 'Create a memorable brand identity with bespoke logos and strategies.',
      icon: '🎨',
      features: ['Logo Design', 'Brand Guidelines', 'Visual Identity']
    },
    {
      id: 2,
      category: 'digital',
      title: 'Digital Marketing',
      description: 'Drive growth with data-driven marketing campaigns across all channels.',
      icon: '📈',
      features: ['SEO', 'Social Media', 'PPC Campaigns']
    },
    {
      id: 3,
      category: 'digital',
      title: 'Web Design & Development',
      description: 'Modern, responsive websites that convert visitors into customers.',
      icon: '💻',
      features: ['Responsive Design', 'E-commerce', 'CMS Integration']
    },
    
    // Premium Services
    {
      id: 4,
      category: 'premium',
      title: 'AI & Chatbots',
      description: 'Intelligent automation and customer service solutions.',
      icon: '🤖',
      features: ['AI Integration', 'Chatbot Development', 'Automation']
    },
    {
      id: 5,
      category: 'premium',
      title: 'Influencer Marketing',
      description: 'Connect with your audience through authentic influencer partnerships.',
      icon: '⭐',
      features: ['Influencer Outreach', 'Campaign Management', 'Analytics']
    },
    {
      id: 6,
      category: 'premium',
      title: 'Video Production',
      description: 'High-quality video content that tells your brand story.',
      icon: '🎬',
      features: ['Corporate Videos', 'Social Media Content', 'Animation']
    },
    
    // Software Development
    {
      id: 7,
      category: 'software',
      title: 'Custom Software Development',
      description: 'Tailored software solutions built for your specific business needs.',
      icon: '⚙️',
      features: ['Custom Applications', 'API Development', 'Integration']
    },
    {
      id: 8,
      category: 'software',
      title: 'Mobile App Development',
      description: 'Native and cross-platform mobile applications.',
      icon: '📱',
      features: ['iOS & Android', 'React Native', 'Flutter']
    },
    {
      id: 9,
      category: 'software',
      title: 'Cloud Solutions',
      description: 'Scalable cloud infrastructure and deployment strategies.',
      icon: '☁️',
      features: ['AWS', 'Azure', 'Cloud Migration']
    }
  ];

  const filteredServices = services.filter(service => {
    const matchesCategory = activeCategory === 'all' || service.category === activeCategory;
    const matchesSearch = service.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         service.description.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  useEffect(() => {
    // Animate cards in when they change
    setVisibleCards([]);
    const timer = setTimeout(() => {
      setVisibleCards(filteredServices.map((_, index) => index));
    }, 100);
    return () => clearTimeout(timer);
  }, [activeCategory, searchTerm]);

  return (
    <section className="py-20 px-4" style={{ background: 'linear-gradient(to bottom, #000000 0%, rgba(196, 211, 34, 0.63) 50%, rgba(196, 211, 34, 0.1) 90%, rgba(196, 211, 34, 0.05) 100%)' }}>
      <div className="max-w-7xl mx-auto">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-6xl font-bold text-white mb-6">
            Our Services
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Comprehensive solutions designed to elevate your business and drive digital transformation
          </p>
        </div>

        {/* Search Bar */}
        <div className="mb-12 max-w-md mx-auto">
          <div className="relative">
            <input
              type="text"
              placeholder="Search services..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-6 py-4 border rounded-full text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:border-transparent transition-all"
              style={{ 
                backgroundColor: '#1a1a1a',
                borderColor: '#c4d322',
                '--tw-ring-color': '#c4d322' 
              }}
            />
            <div className="absolute right-4 top-1/2 transform -translate-y-1/2">
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>
        </div>

        {/* Category Tabs */}
        <div className="mb-16">
          <div className="flex flex-wrap justify-center gap-4">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => setActiveCategory(category.id)}
                className={`px-6 py-3 rounded-full font-semibold transition-all duration-300 ${
                  activeCategory === category.id
                    ? 'text-black shadow-lg'
                    : 'text-gray-300 hover:text-white'
                }`}
                style={
                  activeCategory === category.id 
                    ? { backgroundColor: '#c4d322' } 
                    : { 
                        backgroundColor: '#1a1a1a',
                        border: '1px solid #c4d322'
                      }
                }
              >
                {category.name}
              </button>
            ))}
          </div>
        </div>

        {/* Services Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredServices.map((service, index) => (
            <ServiceCard
              key={service.id}
              service={service}
              index={index}
              isVisible={visibleCards.includes(index)}
              onLearnMore={handleLearnMore}
            />
          ))}
        </div>

        {/* No Results */}
        {filteredServices.length === 0 && (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="text-2xl font-bold text-white mb-4">No services found</h3>
            <p className="text-gray-400">Try adjusting your search or filter criteria</p>
          </div>
        )}
      </div>

      {/* Service Modal */}
      <ServiceModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        serviceId={selectedServiceId}
      />
    </section>
  );
};

export default ServiceSection;
