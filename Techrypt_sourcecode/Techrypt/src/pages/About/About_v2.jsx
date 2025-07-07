import React from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import techryptLogo from "../../assets/Images/techryptLogo.png";

// Fix the import paths - try these alternatives:
// Option 1: If files are in public/IMG folder
import wellnessGif from "/IMG/welness-industry.gif";
import petGif from "/IMG/pet-gif.gif";
import fitnessGif from "/IMG/fitness-gif.gif";

// Option 2: If files are in src/assets/Images folder
// import wellnessGif from "../../assets/Images/welness-industry.gif";
// import petGif from "../../assets/Images/pet-gif.gif";
// import fitnessGif from "../../assets/Images/fitness-gif.gif";

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
      <div className="absolute inset-0 z-0 w-full" style={{ height: 'calc(100vh + 2000px)' }}>
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

   {/* Cross Banners - Attractive & Styled */}
<div className="relative w-full pt-10 pb-24 overflow-visible">
  <div className="absolute inset-0 w-full h-full flex items-center justify-center pointer-events-none">

    {/* First Banner - Top Left to Bottom Right */}
    <div 
      className="absolute w-screen transform rotate-6"
      style={{ left: '50%', transform: 'translateX(-50%) rotate(6deg)' }}
    >
      <div className="bg-gradient-to-r from-yellow-400 via-lime-400 to-yellow-300 py-4 px-6 shadow-2xl rounded-md hover:animate-pulse transition-all duration-500">
        <div className="text-center">
          <span className="text-black font-extrabold text-xl md:text-2xl uppercase tracking-widest drop-shadow-lg">
            AI Vision • Smart Design • Visual Brilliance • AI Innovation • Smart Solutions
          </span>
        </div>
      </div>
    </div>

    {/* Second Banner - Top Right to Bottom Left */}
    <div 
      className="absolute w-screen transform -rotate-6"
      style={{ left: '50%', transform: 'translateX(-50%) rotate(-6deg)' }}
    >
      <div className="bg-gradient-to-r from-yellow-300 via-lime-400 to-yellow-400 py-4 px-6 shadow-2xl rounded-md hover:animate-pulse transition-all duration-500">
        <div className="text-center">
          <span className="text-black font-extrabold text-xl md:text-2xl uppercase tracking-widest drop-shadow-lg">
            Smart Design • AI Innovation • Visual Brilliance • Smart Solutions • AI Vision
          </span>
        </div>
      </div>
    </div>

  </div>
</div>
{/* Revolutionizing AI Implementations Section - Mobile Responsive */}
<section className="py-16 md:py-20 bg-transparent relative z-5">
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
        <div className="relative bg-gradient-to-br from-primary/20 to-primary/5 rounded-2xl p-4 sm:p-6 md:p-8 border border-primary/30">
          
          <div className="aspect-square w-48 sm:w-64 md:w-72 mx-auto bg-gradient-to-br from-primary/10 to-transparent rounded-full flex items-center justify-center">
            <img 
              src={techryptLogo} 
              alt="Techrypt Logo" 
              className="w-32 sm:w-40 md:w-48 h-auto object-contain filter brightness-0 invert" 
            />
          </div>

          {/* Blur Elements */}
          <div className="absolute -top-3 -right-3 w-12 h-12 sm:w-16 sm:h-16 bg-primary/20 rounded-full blur-xl"></div>
          <div className="absolute -bottom-3 -left-3 w-10 h-10 sm:w-14 sm:h-14 bg-primary/30 rounded-full blur-lg"></div>
        </div>
      </motion.div>

      {/* Right Column - Remains same */}
      {/* Keep your content block here without changes */}

            
            {/* Right Column - Content */}
            {/* Right Column - Content */}
<motion.div
  initial={{ opacity: 0, x: 50 }}
  whileInView={{ opacity: 1, x: 0 }}
  viewport={{ once: true }}
  transition={{ duration: 0.8 }}
>
  <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-4 sm:mb-6 leading-snug">
    Revolutionizing <span className="text-primary">AI Implementations</span>
  </h2>

  <p className="text-base sm:text-lg md:text-xl text-gray-300 mb-6 sm:mb-8">
    Transforming businesses through intelligent automation and cutting-edge technology solutions
  </p>

  <div className="space-y-3 sm:space-y-4 mb-6 sm:mb-8">
    {[
      "Advanced AI-powered automation systems",
      "Scalable solutions for businesses of all sizes",
      "24/7 support and continuous optimization",
      "Proven ROI and measurable results"
    ].map((text, i) => (
      <div key={i} className="flex items-start gap-3">
        <div className="w-5 h-5 sm:w-6 sm:h-6 bg-primary rounded-full flex items-center justify-center mt-0.5">
          <span className="text-black font-bold text-xs sm:text-sm">✓</span>
        </div>
        <span className="text-sm sm:text-base text-gray-300">{text}</span>
      </div>
    ))}
  </div>

  <button 
    onClick={openContactForm}
    className="bg-primary hover:bg-primaryLight text-black font-bold py-3 px-6 sm:py-4 sm:px-8 rounded-full transition duration-300 transform hover:scale-105 w-full sm:w-auto"
  >
    Learn More
  </button>
</motion.div>

          </div>
        </div>

      </section>
<section className="relative py-16 sm:py-20 pb-0 bg-transparent overflow-hidden z-5">
  <div className="container-responsive px-4 relative z-5">
    <motion.div
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true }}
      variants={fadeIn}
      className="text-center max-w-4xl mx-auto"
    >
      <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-6 sm:mb-8">
        Our <span className="text-primary">Vision</span>
      </h2>

      <div className="bg-black/50 backdrop-blur-sm border-2 border-primary/30 rounded-2xl p-6 sm:p-8 md:p-12">
        <p className="text-base sm:text-lg md:text-2xl text-white leading-relaxed">
          We envision a future where artificial intelligence seamlessly integrates into every aspect of business operations,
          empowering organizations to achieve unprecedented levels of efficiency, innovation, and growth. Our mission is to
          democratize AI technology, making powerful automation accessible to businesses of all sizes while maintaining the
          human touch that drives meaningful connections and exceptional experiences.
        </p>
      </div>
    </motion.div>
  </div>
</section>
  {/* Industries We Target Section */}
      <section className="py-20 relative z-5">
        <div className="container-responsive px-4">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeIn}
            className="text-center mb-16"
          >
            {/* Floating Heading */}
            <div className="relative mb-12">
              <motion.h2 
                className="text-4xl md:text-5xl font-bold text-white mb-4"
                animate={{ 
                  y: [0, -10, 0],
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              >
                Industries We <span className="text-primary">Specifically Target</span>
              </motion.h2>
              
              {/* Bouncing Ball Animation */}
              <motion.div
                className="absolute top-full left-1/2 transform -translate-x-1/2 w-4 h-4 bg-primary rounded-full"
                animate={{
                  x: [0, 200, 400, 200, 0],
                  y: [0, -20, 0, -15, 0],
                }}
                transition={{
                  duration: 4,
                  repeat: Infinity,
                  ease: "easeInOut",
                  times: [0, 0.25, 0.5, 0.75, 1]
                }}
              />
            </div>

            {/* Industry Cards Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
              
              {/* Pet Industry Card - CLICKABLE */}
              <motion.div
                className="bg-black border-2 border-primary/30 rounded-2xl p-6 hover:border-primary/60 transition-all duration-300 relative overflow-hidden group cursor-pointer"
                variants={cardVariant}
                whileHover={{ scale: 1.05 }}
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                onClick={() => window.location.href = '/LandingPages/PetLandingPage'}
              >
                {/* Bouncing Ball for Pet Industry */}
                <motion.div
                  className="absolute top-4 right-4 w-3 h-3 bg-primary rounded-full"
                  animate={{
                    y: [0, -15, 0],
                  }}
                  transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    ease: "easeInOut",
                    delay: 0
                  }}
                />
                
                <div className="aspect-video mb-6 rounded-xl overflow-hidden bg-gray-900">
                  <img 
                    src={petGif}
                    alt="Pet Industry Solutions"
                    className="w-full h-full object-cover"
                  />
                </div>
                
                <div className="text-center">
                  <h3 className="text-2xl font-bold text-primary mb-3">Pet Industry</h3>
                  <p className="text-gray-300 mb-4">
                    Revolutionizing pet care with AI-powered booking systems, customer management, and automated marketing for veterinary clinics, grooming services, and pet stores.
                  </p>
                  <div className="flex flex-wrap justify-center gap-2 mb-4">
                    <span className="bg-primary/20 text-primary px-3 py-1 rounded-full text-sm">Pet Care</span>
                    <span className="bg-primary/20 text-primary px-3 py-1 rounded-full text-sm">Veterinary</span>
                    <span className="bg-primary/20 text-primary px-3 py-1 rounded-full text-sm">Grooming</span>
                  </div>
                  {/* Click indicator */}
                  <div className="text-primary text-sm font-semibold opacity-70 group-hover:opacity-100 transition-opacity">
                    Click to explore Pet Solutions →
                  </div>
                </div>
              </motion.div>

              {/* Wellness/Spa Industry Card - NOT CLICKABLE YET */}
              <motion.div
                className="bg-black border-2 border-primary/30 rounded-2xl p-6 hover:border-primary/60 transition-all duration-300 relative overflow-hidden group"
                variants={cardVariant}
                whileHover={{ scale: 1.05 }}
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
              >
                {/* Bouncing Ball for Wellness Industry */}
                <motion.div
                  className="absolute top-4 right-4 w-3 h-3 bg-primary rounded-full"
                  animate={{
                    y: [0, -15, 0],
                  }}
                  transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    ease: "easeInOut",
                    delay: 0.5
                  }}
                />
                
                <div className="aspect-video mb-6 rounded-xl overflow-hidden bg-gray-900">
                  <img 
                    src={wellnessGif}
                    alt="Wellness & Spa Industry Solutions"
                    className="w-full h-full object-cover"
                  />
                </div>
                
                <div className="text-center">
                  <h3 className="text-2xl font-bold text-primary mb-3">Wellness & Spa</h3>
                  <p className="text-gray-300 mb-4">
                    Enhancing relaxation experiences with intelligent appointment scheduling, personalized treatment recommendations, and seamless customer journey automation.
                  </p>
                  <div className="flex flex-wrap justify-center gap-2 mb-4">
                    <span className="bg-primary/20 text-primary px-3 py-1 rounded-full text-sm">Spa Services</span>
                    <span className="bg-primary/20 text-primary px-3 py-1 rounded-full text-sm">Massage</span>
                    <span className="bg-primary/20 text-primary px-3 py-1 rounded-full text-sm">Wellness</span>
                  </div>
                  {/* Coming soon indicator */}
                  <div className="text-gray-500 text-sm font-semibold">
                    Landing Page Coming Soon
                  </div>
                </div>
              </motion.div>

              {/* Fitness Industry Card - CLICKABLE */}
              <motion.div
                className="bg-black border-2 border-primary/30 rounded-2xl p-6 hover:border-primary/60 transition-all duration-300 relative overflow-hidden group cursor-pointer"
                variants={cardVariant}
                whileHover={{ scale: 1.05 }}
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                onClick={() => window.location.href = '/LandingPages/FitnessLandingPage'}
              >
                {/* Bouncing Ball for Fitness Industry */}
                <motion.div
                  className="absolute top-4 right-4 w-3 h-3 bg-primary rounded-full"
                  animate={{
                    y: [0, -15, 0],
                  }}
                  transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    ease: "easeInOut",
                    delay: 1
                  }}
                />
                
                <div className="aspect-video mb-6 rounded-xl overflow-hidden bg-gray-900">
                  <img 
                    src={fitnessGif}
                    alt="Fitness Industry Solutions"
                    className="w-full h-full object-cover"
                  />
                </div>
                
                <div className="text-center">
                  <h3 className="text-2xl font-bold text-primary mb-3">Fitness Industry</h3>
                  <p className="text-gray-300 mb-4">
                    Empowering fitness centers with smart member management, AI-driven workout plans, and automated progress tracking for enhanced member experiences.
                  </p>
                  <div className="flex flex-wrap justify-center gap-2 mb-4">
                    <span className="bg-primary/20 text-primary px-3 py-1 rounded-full text-sm">Gym Management</span>
                    <span className="bg-primary/20 text-primary px-3 py-1 rounded-full text-sm">Personal Training</span>
                    <span className="bg-primary/20 text-primary px-3 py-1 rounded-full text-sm">Fitness Apps</span>
                  </div>
                  {/* Click indicator */}
                  <div className="text-primary text-sm font-semibold opacity-70 group-hover:opacity-100 transition-opacity">
                    Click to explore Fitness Solutions →
                  </div>
                </div>
              </motion.div>

            </div>
            
            {/* Additional floating text */}
            <motion.p 
              className="text-lg text-gray-400 mt-12 max-w-3xl mx-auto"
              animate={{ 
                opacity: [0.7, 1, 0.7],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            >
              These industries represent our core expertise where we've delivered transformative AI solutions that drive real business results.
            </motion.p>
          </motion.div>
        </div>
      </section> 

   <section className="py-16 sm:py-20 relative z-5">
    <div className="container-responsive px-4">
      <motion.div
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={fadeIn}
        className="text-center mb-12 sm:mb-16"
      >
        <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-6 sm:mb-8">
          Our <span className="text-primary">Team</span>
        </h2>

        <div className="max-w-4xl mx-auto">
          <p className="text-base sm:text-xl md:text-2xl text-gray-300 mb-6 sm:mb-8">
            We are a diverse collective of visionaries, engineers, and creatives brought together by our shared passion for
            artificial intelligence and emerging technologies. Our team spans across continents, cultures, and disciplines,
            united by a common goal: to push the boundaries of what's possible in the digital realm.
          </p>

          <p className="text-sm sm:text-lg text-gray-400 mb-10 sm:mb-12">
            From seasoned AI researchers to innovative designers, from strategic business minds to hands-on developers,
            each member of our team brings unique expertise and perspective.
          </p>

          {/* Team Cards with stagger animation */}
          <motion.div
            variants={staggerContainer}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 sm:gap-8"
          >
            {[
              {
                title: "AI Specialists",
                icon: (
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10" />
                ),
                desc: "Machine learning engineers and data scientists pushing the boundaries of AI"
              },
              {
                title: "Creative Minds",
                icon: (
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87" />
                ),
                desc: "Designers and strategists crafting beautiful, user-centered experiences"
              },
              {
                title: "Tech Innovators",
                icon: (
                  <path d="M20 3H4c-1.1 0-2 .9-2 2v11" />
                ),
                desc: "Full-stack developers and system architects building the future"
              }
            ].map(({ title, icon, desc }, idx) => (
              <motion.div
                key={idx}
                className="bg-black border-2 border-primary/30 rounded-xl p-5 sm:p-6 hover:border-primary/60 transition-all duration-300"
                variants={cardVariant}
                whileHover={{ scale: 1.05 }}
              >
                <div className="w-14 h-14 mx-auto mb-4 bg-primary/20 rounded-full flex items-center justify-center">
                  <svg className="w-7 h-7 text-primary" fill="currentColor" viewBox="0 0 24 24">
                    {icon}
                  </svg>
                </div>
                <h3 className="text-lg sm:text-xl font-bold text-primary mb-2 text-center">{title}</h3>
                <p className="text-sm sm:text-base text-gray-300 text-center">{desc}</p>
              </motion.div>
            ))}
          </motion.div>
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