import React from 'react';
import { motion } from 'framer-motion';

const BusinessVerticals = () => {
  // Function to open chatbot with contextual message
  const openChatbotWithContext = (businessType) => {
    // Dispatch custom event to trigger chatbot opening
    const event = new CustomEvent('openTechryptChatbot', {
      detail: {
        contextMessage: `How can I help you with ${businessType} solutions?`,
        businessType: businessType
      }
    });
    window.dispatchEvent(event);
  };

  const verticals = [
    {
      title: "E-commerce & Online Retail",
      description: "Complete digital solutions for online stores, marketplace optimization, and payment integration.",
      services: ["Website Development", "Payment Gateway", "Social Media Marketing"],
      icon: "/Images/ecommerce.jpeg"
    },
    {
      title: "Restaurants & Food Services",
      description: "Digital solutions to boost your restaurant's online presence and customer engagement.",
      services: ["Website Development", "Social Media Marketing", "Chatbot Development"],
      icon: "/Images/restaurant.png"
    },
    {
      title: "Healthcare & Medical",
      description: "HIPAA-compliant digital solutions for healthcare providers and medical practices.",
      services: ["Website Development", "Automation Packages", "Chatbot Development"],
      icon: "/Images/healthcare.jpeg"
    },
    {
      title: "Beauty Salons & Spas",
      description: "Showcase your work and streamline bookings with our specialized beauty industry solutions.",
      services: ["Social Media Marketing", "Website Development", "Automation Packages"],
      icon: "/Images/spa.jpg"
    },
    {
      title: "Fitness & Wellness",
      description: "Build community and manage memberships with our fitness-focused digital solutions.",
      services: ["Social Media Marketing", "Website Development", "Automation Packages"],
      icon: "/Images/fitness.jpeg"
    },
    {
      title: "Professional Services",
      description: "Establish credibility and attract clients with professional digital presence.",
      services: ["Website Development", "Branding Services", "Chatbot Development"],
      icon: "/Images/professional.jpg"
    },
    {
      title: "Real Estate",
      description: "Showcase properties and generate leads with our real estate digital solutions.",
      services: ["Website Development", "Social Media Marketing", "Automation Packages"],
      icon: "/Images/realestate.jpg"
    },
    {
      title: "Technology Companies",
      description: "Advanced digital solutions for tech companies and startups looking to scale.",
      services: ["Website Development", "Branding Services", "Automation Packages"],
      icon: "/Images/tech.jpeg"
    }
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5
      }
    }
  };

  return (
    <section className="py-20 px-4 bg-[#0f0f0f]">
      <div className="max-w-7xl mx-auto">
        {/* Section Header */}
        <motion.div 
          className="text-center mb-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Industries We <span className="text-primary">Serve</span>
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Specialized digital solutions tailored to your industry's unique needs and challenges
          </p>
        </motion.div>

        {/* Verticals Grid */}
        <motion.div 
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          {verticals.map((vertical, index) => (
            <motion.div
              key={index}
              variants={itemVariants}
              className="bg-[#1a1a1a] border border-gray-800 rounded-lg p-6 hover:border-primary transition-all duration-300 group cursor-pointer"
              whileHover={{ y: -5 }}
              onClick={() => openChatbotWithContext(vertical.title)}
            >
              {/* Centering the image using flexbox */}
              <div className="flex justify-center items-center mb-4">
                {typeof vertical.icon === 'string' && vertical.icon.includes('/') ? (
                  <img src={vertical.icon} alt={vertical.title} className="w-45 h-32 object-cover rounded" />
                ) : (
                  vertical.icon
                )}
              </div>
              <h3 className="text-xl font-semibold text-white mb-3 group-hover:text-primary transition-colors">
                {vertical.title}
              </h3>
              <p className="text-gray-400 mb-4 text-sm leading-relaxed">
                {vertical.description}
              </p>
              <div className="mt-4">
                <button className="text-primary font-medium text-sm hover:text-primary/80 transition-colors">
                  Get Custom Solution →
                </button>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Call to Action */}
        <motion.div 
          className="text-center mt-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          viewport={{ once: true }}
        >
          <p className="text-lg text-gray-300 mb-6">
            Don't see your industry? We work with businesses of all types and sizes.
          </p>
          <motion.button
            className="bg-primary text-black px-8 py-3 rounded-lg font-semibold hover:bg-primary/90 transition-colors"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => openChatbotWithContext('Custom Business')}
          >
            Get Custom Solution
          </motion.button>
        </motion.div>

        {/* Platforms Section */}
        <motion.div 
          className="mt-20 text-center"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h3 className="text-2xl font-bold text-white mb-8">
            Platforms We <span className="text-primary">Integrate With</span>
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
            {[ 
              "Shopify", "Amazon", "eBay", "Etsy", 
              "Daraz", "Facebook", "Instagram", "TikTok"
            ].map((platform, index) => (
              <motion.div
                key={index}
                className="bg-[#1a1a1a] border border-gray-800 rounded-lg p-4 hover:border-primary transition-all duration-300"
                whileHover={{ y: -3 }}
              >
                <p className="text-white font-medium text-sm">{platform}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default BusinessVerticals;
