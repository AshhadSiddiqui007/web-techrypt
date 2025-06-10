import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const OtherWorks = () => {
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  // Function to open chatbot with contextual message
  const openChatbotWithContext = (message) => {
    const event = new CustomEvent('openTechryptChatbot', {
      detail: {
        contextMessage: message,
        businessType: 'Project Inquiry'
      }
    });
    window.dispatchEvent(event);
  };

  // Hardcoded project details for each project
  const getProjectDetails = (projectId) => {
    const projectDetails = {
      1: `🚀 TechCorp E-commerce Platform Details:

• Complete e-commerce solution with advanced features
• Payment integration with Stripe and PayPal
• Real-time inventory management system
• Mobile-responsive design with PWA capabilities
• Admin dashboard with analytics and reporting
• Customer reviews and rating system
• Multi-language and multi-currency support

Technologies: React, Node.js, Stripe, MongoDB
Timeline: 3-4 months
Client: TechCorp Solutions

Would you like to discuss a similar e-commerce project for your business?`,

      2: `🏥 HealthCare Pro Website Details:

• HIPAA-compliant healthcare website
• Secure patient portal with appointment booking
• Electronic health records integration
• Telemedicine video consultation features
• Insurance verification system
• Prescription management portal
• Mobile app for patients and doctors

Technologies: React, Express, PostgreSQL, AWS
Timeline: 4-5 months
Client: HealthCare Pro

Would you like to discuss a healthcare website for your practice?`,

      3: `📱 FoodieDelight Social Campaign Details:

• Comprehensive social media strategy across platforms
• 300% increase in engagement within 6 months
• User-generated content campaigns
• Influencer partnerships and collaborations
• Food photography and video content creation
• Instagram Stories and Reels optimization
• Analytics and performance tracking

Platforms: Instagram, Facebook, TikTok, Analytics
Timeline: 6 months ongoing
Client: FoodieDelight Restaurant

Would you like to discuss a social media strategy for your restaurant?`,

      4: `💄 BeautyBliss Brand Identity Details:

• Complete brand redesign and identity creation
• Modern logo design with multiple variations
• Color palette and typography guidelines
• Marketing materials (business cards, brochures, signage)
• Social media templates and brand assets
• Website design mockups
• Brand guidelines documentation

Tools: Adobe Creative Suite, Figma, Brand Guidelines
Timeline: 2-3 months
Client: BeautyBliss Salon

Would you like to discuss a brand identity project for your business?`,

      5: `🤖 AI Customer Support Bot Details:

• Intelligent chatbot with natural language processing
• 24/7 automated customer support
• Appointment booking and scheduling integration
• Multi-language support capabilities
• CRM integration for customer data management
• Analytics dashboard for bot performance
• Custom training for industry-specific queries

Technologies: Python, NLP, MongoDB, React
Timeline: 2-3 months
Client: Multiple Clients

Would you like to discuss an AI chatbot for your business?`,

      6: `💪 FitLife Mobile App Details:

• Comprehensive fitness tracking mobile application
• Personalized workout plans and routines
• Nutrition guidance and meal planning
• Progress tracking with charts and analytics
• Social features for community engagement
• Integration with wearable devices
• In-app purchases for premium features

Technologies: React Native, Firebase, Redux, API Integration
Timeline: 4-6 months
Client: FitLife Gym

Would you like to discuss a mobile app for your fitness business?`
    };

    return projectDetails[projectId] || 'For detailed project information, please book an appointment to discuss this project';
  };

  const categories = [
    'All',
    'Website Development',
    'E-commerce',
    'Social Media Marketing',
    'Branding',
    'Chatbot Development',
    'Mobile Apps',
    'Automation'
  ];

  const projects = [
    {
      id: 1,
      title: "TechCorp E-commerce Platform",
      category: "E-commerce",
      description: "Complete e-commerce solution with payment integration and inventory management",
      image: "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=300&fit=crop",
      technologies: ["React", "Node.js", "Stripe", "MongoDB"],
      client: "TechCorp Solutions",
      year: "2024"
    },
    {
      id: 2,
      title: "HealthCare Pro Website",
      category: "Website Development",
      description: "HIPAA-compliant healthcare website with appointment booking system",
      image: "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400&h=300&fit=crop",
      technologies: ["React", "Express", "PostgreSQL", "AWS"],
      client: "HealthCare Pro",
      year: "2024"
    },
    {
      id: 3,
      title: "FoodieDelight Social Campaign",
      category: "Social Media Marketing",
      description: "Comprehensive social media strategy that increased engagement by 300%",
      image: "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400&h=300&fit=crop",
      technologies: ["Instagram", "Facebook", "TikTok", "Analytics"],
      client: "FoodieDelight Restaurant",
      year: "2023"
    },
    {
      id: 4,
      title: "BeautyBliss Brand Identity",
      category: "Branding",
      description: "Complete brand redesign including logo, color palette, and marketing materials",
      image: "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400&h=300&fit=crop",
      technologies: ["Adobe Creative Suite", "Figma", "Brand Guidelines"],
      client: "BeautyBliss Salon",
      year: "2024"
    },
    {
      id: 5,
      title: "AI Customer Support Bot",
      category: "Chatbot Development",
      description: "Intelligent chatbot with natural language processing and appointment booking",
      image: "https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=400&h=300&fit=crop",
      technologies: ["Python", "NLP", "MongoDB", "React"],
      client: "Multiple Clients",
      year: "2024"
    },
    {
      id: 6,
      title: "FitLife Mobile App",
      category: "Mobile Apps",
      description: "Fitness tracking app with workout plans and nutrition guidance",
      image: "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop",
      technologies: ["React Native", "Firebase", "Redux", "API Integration"],
      client: "FitLife Gym",
      year: "2023"
    },
    {
      id: 7,
      title: "AutoFlow Business Suite",
      category: "Automation",
      description: "Complete business process automation including CRM and email marketing",
      image: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=300&fit=crop",
      technologies: ["Zapier", "HubSpot", "Mailchimp", "Custom APIs"],
      client: "AutoFlow Inc",
      year: "2024"
    },
    {
      id: 8,
      title: "RetailMax Online Store",
      category: "E-commerce",
      description: "Multi-vendor marketplace with advanced filtering and payment options",
      image: "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=300&fit=crop",
      technologies: ["Shopify Plus", "Custom Apps", "Payment Gateways"],
      client: "RetailMax",
      year: "2023"
    }
  ];

  // Filter projects based on selected category and limit to 6 maximum
  const filteredProjects = (selectedCategory === 'All'
    ? projects
    : projects.filter(project => project.category === selectedCategory)
  ).slice(0, 6); // Limit to 6 projects maximum

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
          className="text-center mb-12"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Our <span className="text-primary">Recent Works</span>
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-8">
            Explore our portfolio of successful projects across various industries and technologies
          </p>

          {/* Filter Dropdown */}
          <div className="relative inline-block">
            <motion.button
              className="bg-[#1a1a1a] border border-gray-700 text-white px-6 py-3 rounded-lg flex items-center gap-2 hover:border-primary transition-colors"
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <span>Filter by: {selectedCategory}</span>
              <motion.svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                animate={{ rotate: isDropdownOpen ? 180 : 0 }}
                transition={{ duration: 0.2 }}
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </motion.svg>
            </motion.button>

            <AnimatePresence>
              {isDropdownOpen && (
                <motion.div
                  className="absolute top-full left-0 mt-2 w-64 bg-[#1a1a1a] border border-gray-700 rounded-lg shadow-xl z-50"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.2 }}
                >
                  {categories.map((category) => (
                    <motion.button
                      key={category}
                      className={`w-full text-left px-4 py-3 hover:bg-primary/10 transition-colors ${
                        selectedCategory === category ? 'text-primary bg-primary/5' : 'text-white'
                      }`}
                      onClick={() => {
                        setSelectedCategory(category);
                        setIsDropdownOpen(false);
                      }}
                      whileHover={{ x: 5 }}
                    >
                      {category}
                    </motion.button>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>

        {/* Projects Grid */}
        <motion.div 
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          key={selectedCategory} // Re-animate when category changes
        >
          <AnimatePresence mode="wait">
            {filteredProjects.map((project) => (
              <motion.div
                key={project.id}
                variants={itemVariants}
                className="bg-[#1a1a1a] border border-gray-800 rounded-lg overflow-hidden hover:border-primary transition-all duration-300 group"
                whileHover={{ y: -5 }}
                layout
              >
                {/* Project Image */}
                <div className="relative h-48 overflow-hidden">
                  <img
                    src={project.image}
                    alt={project.title}
                    className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'flex';
                    }}
                  />
                  <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-purple-600/20 hidden items-center justify-center">
                    <div className="text-6xl opacity-50">🚀</div>
                  </div>
                  <div className="absolute top-4 right-4 bg-primary text-black px-2 py-1 rounded text-xs font-semibold">
                    {project.year}
                  </div>
                </div>

                {/* Project Content */}
                <div className="p-6">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-primary text-sm font-medium">{project.category}</span>
                    <span className="text-gray-500 text-sm">{project.client}</span>
                  </div>
                  
                  <h3 className="text-xl font-semibold text-white mb-3 group-hover:text-primary transition-colors">
                    {project.title}
                  </h3>
                  
                  <p className="text-gray-400 mb-4 text-sm leading-relaxed">
                    {project.description}
                  </p>

                  {/* Technologies */}
                  <div className="flex flex-wrap gap-2 mb-4">
                    {project.technologies.slice(0, 3).map((tech, index) => (
                      <span 
                        key={index}
                        className="text-xs bg-gray-800 text-gray-300 px-2 py-1 rounded"
                      >
                        {tech}
                      </span>
                    ))}
                    {project.technologies.length > 3 && (
                      <span className="text-xs text-gray-500">
                        +{project.technologies.length - 3} more
                      </span>
                    )}
                  </div>

                  {/* View Project Details Button */}
                  <motion.button
                    className="w-full bg-primary/10 text-primary py-2 rounded-lg font-medium hover:bg-primary hover:text-black transition-all duration-300"
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => openChatbotWithContext(getProjectDetails(project.id))}
                  >
                    View Project Details
                  </motion.button>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </motion.div>

        {/* No Results Message */}
        {filteredProjects.length === 0 && (
          <motion.div 
            className="text-center py-12"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <p className="text-gray-400 text-lg">No projects found in this category.</p>
          </motion.div>
        )}

        {/* Call to Action */}
        <motion.div 
          className="text-center mt-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          viewport={{ once: true }}
        >
          <h3 className="text-2xl font-bold text-white mb-4">
            Ready to Start Your Project?
          </h3>
          <p className="text-gray-300 mb-6">
            Let's discuss how we can bring your vision to life with our expertise.
          </p>
          <motion.button
            className="bg-primary text-black px-8 py-3 rounded-lg font-semibold hover:bg-primary/90 transition-colors"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => openChatbotWithContext("Let's discuss your project requirements and schedule a consultation")}
          >
            Start Your Project
          </motion.button>
        </motion.div>
      </div>
    </section>
  );
};

export default OtherWorks;
