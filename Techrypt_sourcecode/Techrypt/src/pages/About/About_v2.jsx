import React from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import techryptLogo from "../../assets/Images/techryptLogo.png";

const About_v2 = () => {
  // Animation variants
  const fadeIn = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.8 }
    }
  };

  const staggerContainer = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
        delayChildren: 0.3
      }
    }
  };

  const cardVariant = {
    hidden: { opacity: 0, scale: 0.8 },
    visible: {
      opacity: 1,
      scale: 1,
      transition: {
        type: "spring",
        stiffness: 100,
        damping: 10
      }
    }
  };

  // Open contact form function
  const openContactForm = () => {
    const event = new CustomEvent('openTechryptChatbot', {
      detail: {
        contextMessage: "Hi there! I'd like to learn more about Techrypt's services.",
        businessType: 'About Page Visitor',
        showAppointmentForm: true
      }
    });
    window.dispatchEvent(event);
  };

  return (
    <div className="bg-black min-h-screen relative">
      {/* Animated Green Gradient Background for main content only */}
      <div className="absolute inset-0 z-0 w-full" style={{ height: 'calc(100vh + 1600px)' }}>
        <div className="absolute inset-0 w-full h-full animate-gradient-move"></div>
      </div>

      {/* Hero Section with Animated Green Gradient */}
      <section className="relative h-[65vh] flex items-center justify-center overflow-hidden z-5">
        <div className="container-responsive z-20 text-center px-4">
          <motion.div
            initial="hidden"
            animate="visible"
            variants={fadeIn}
          >
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-black text-white mb-6 uppercase tracking-wider">
              About <span className="text-primary">Us</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-200 max-w-3xl mx-auto mb-6">
              Leading the future of AI innovation and digital transformation
            </p>
          </motion.div>
        </div>
      </section>

      {/* Cross Banners - With Proper Spacing */}
      <div className="relative w-full pt-5 pb-20 overflow-visible">
        <div className="absolute inset-0 w-full h-full flex items-center justify-center">
          {/* First Banner - Top Left to Bottom Right */}
          <div className="absolute transform rotate-6 w-screen" style={{ left: '50%', transform: 'translateX(-50%) rotate(6deg)' }}>
            <div className="bg-primary py-4 shadow-lg">
              <div className="text-center">
                <span className="text-black font-bold text-2xl uppercase tracking-wider">
                  AI Vision • Smart Design • Visual Brilliance • AI Innovation • Smart Solutions
                </span>
              </div>
            </div>
          </div>
          
          {/* Second Banner - Top Right to Bottom Left */}
          <div className="absolute transform -rotate-6 w-screen" style={{ left: '50%', transform: 'translateX(-50%) rotate(-6deg)' }}>
            <div className="bg-primary py-4 shadow-lg">
              <div className="text-center">
                <span className="text-black font-bold text-2xl uppercase tracking-wider">
                  Smart Design • AI Innovation • Visual Brilliance • Smart Solutions • AI Vision
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Revolutionizing AI Implementations Section */}
      <section className="py-20 bg-transparent relative z-5 ">
        <div className="container-responsive px-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Left Column - Image/Graphic */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
              className="relative"
            >
              <div className="relative bg-gradient-to-br from-primary/20 to-primary/5 rounded-2xl p-8 border border-primary/30">
                <div className="aspect-square bg-gradient-to-br from-primary/10 to-transparent rounded-full flex items-center justify-center">
                  <img 
                    src={techryptLogo} 
                    alt="Techrypt Logo" 
                    className="w-120 h-120 object-contain filter brightness-0 invert" 
                  />
                </div>
                <div className="absolute -top-4 -right-4 w-20 h-20 bg-primary/20 rounded-full blur-xl"></div>
                <div className="absolute -bottom-4 -left-4 w-16 h-16 bg-primary/30 rounded-full blur-lg"></div>
              </div>
            </motion.div>
            
            {/* Right Column - Content */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
            >
              <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
                Revolutionizing <span className="text-primary">AI Implementations</span>
              </h2>
              
              <p className="text-xl text-gray-300 mb-8">
                Transforming businesses through intelligent automation and cutting-edge technology solutions
              </p>
              
              <div className="space-y-4 mb-8">
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-primary rounded-full flex items-center justify-center mt-1">
                    <span className="text-black font-bold text-sm">✓</span>
                  </div>
                  <span className="text-gray-300">Advanced AI-powered automation systems</span>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-primary rounded-full flex items-center justify-center mt-1">
                    <span className="text-black font-bold text-sm">✓</span>
                  </div>
                  <span className="text-gray-300">Scalable solutions for businesses of all sizes</span>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-primary rounded-full flex items-center justify-center mt-1">
                    <span className="text-black font-bold text-sm">✓</span>
                  </div>
                  <span className="text-gray-300">24/7 support and continuous optimization</span>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-primary rounded-full flex items-center justify-center mt-1">
                    <span className="text-black font-bold text-sm">✓</span>
                  </div>
                  <span className="text-gray-300">Proven ROI and measurable results</span>
                </div>
              </div>
              
              <button 
                onClick={openContactForm}
                className="bg-primary hover:bg-primaryLight text-black font-bold py-4 px-8 rounded-full transition duration-300 transform hover:scale-105"
              >
                Learn More
              </button>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Our Vision Section with Animated Gradient */}
      <section className="relative py-20 bg-transparent overflow-hidden z-5">          
        <div className="container-responsive px-4 relative z-5">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeIn}
            className="text-center max-w-4xl mx-auto"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-8">
              Our <span className="text-primary">Vision</span>
            </h2>
            
            <div className="bg-black/50 backdrop-blur-sm border-2 border-primary/30 rounded-2xl p-8 md:p-12">
              <p className="text-xl md:text-2xl text-white leading-relaxed">
                We envision a future where artificial intelligence seamlessly integrates into every aspect of business operations, 
                empowering organizations to achieve unprecedented levels of efficiency, innovation, and growth. Our mission is to 
                democratize AI technology, making powerful automation accessible to businesses of all sizes while maintaining the 
                human touch that drives meaningful connections and exceptional experiences.
              </p>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Our Team Section */}
      <section className="py-20 relative z-5">
        <div className="container-responsive px-4">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeIn}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-8">
              Our <span className="text-primary">Team</span>
            </h2>
            
            <div className="max-w-4xl mx-auto">
              <p className="text-xl md:text-2xl text-gray-300 mb-8">
                We are a diverse collective of visionaries, engineers, and creatives brought together by our shared passion for 
                artificial intelligence and emerging technologies. Our team spans across continents, cultures, and disciplines, 
                united by a common goal: to push the boundaries of what's possible in the digital realm.
              </p>
              
              <p className="text-lg text-gray-400 mb-12">
                From seasoned AI researchers to innovative designers, from strategic business minds to hands-on developers, 
                each member of our team brings unique expertise and perspective. We believe that the most groundbreaking 
                solutions emerge when diverse minds collaborate, challenge assumptions, and dare to reimagine the future 
                of technology.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <motion.div
                  className="bg-black border-2 border-primary/30 rounded-xl p-6 hover:border-primary/60 transition-all duration-300"
                  variants={cardVariant}
                  whileHover={{ scale: 1.05 }}
                >
                  <div className="text-4xl mb-4 text-center">🧠</div>
                  <h3 className="text-xl font-bold text-primary mb-2 text-center">AI Specialists</h3>
                  <p className="text-gray-300 text-center">Machine learning engineers and data scientists pushing the boundaries of AI</p>
                </motion.div>
                
                <motion.div
                  className="bg-black border-2 border-primary/30 rounded-xl p-6 hover:border-primary/60 transition-all duration-300"
                  variants={cardVariant}
                  whileHover={{ scale: 1.05 }}
                >
                  <div className="text-4xl mb-4 text-center">🎨</div>
                  <h3 className="text-xl font-bold text-primary mb-2 text-center">Creative Minds</h3>
                  <p className="text-gray-300 text-center">Designers and strategists crafting beautiful, user-centered experiences</p>
                </motion.div>
                
                <motion.div
                  className="bg-black border-2 border-primary/30 rounded-xl p-6 hover:border-primary/60 transition-all duration-300"
                  variants={cardVariant}
                  whileHover={{ scale: 1.05 }}
                >
                  <div className="text-4xl mb-4 text-center">⚡</div>
                  <h3 className="text-xl font-bold text-primary mb-2 text-center">Tech Innovators</h3>
                  <p className="text-gray-300 text-center">Full-stack developers and system architects building the future</p>
                </motion.div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Call to Action Section */}
      <section className="py-20 bg-black relative z-5">
        <div className="container-responsive px-4">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeIn}
            className="max-w-4xl mx-auto text-center"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Ready to <span className="text-primary">Transform</span> Your Business?
            </h2>
            <p className="text-xl text-gray-300 mb-10">
              Let's discuss how our AI-powered solutions can help you achieve your goals
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Link 
                to="/contact" 
                className="bg-primary hover:bg-primaryLight text-black font-bold py-4 px-8 rounded-full transition duration-300 transform hover:scale-105"
              >
                Contact Us
              </Link>
              <button 
                onClick={openContactForm}
                className="bg-transparent hover:bg-primary/10 text-primary border-2 border-primary font-bold py-4 px-8 rounded-full transition duration-300 transform hover:scale-105"
              >
                Chat With Us
              </button>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default About_v2;