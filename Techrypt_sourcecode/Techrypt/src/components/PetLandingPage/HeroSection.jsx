import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle } from 'lucide-react';
import PetChatUI from './PetChatUI';

const HeroSection = ({ onGetStarted, fadeInUp, staggerContainer }) => {

  return (
    <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <motion.div 
          variants={staggerContainer}
          initial="initial"
          animate="animate"
          className="grid lg:grid-cols-2 gap-12 items-center"
        >
          <div className="space-y-8">
            <motion.div variants={fadeInUp} className="space-y-6">
              <h1 className="text-5xl lg:text-7xl font-bold leading-tight">
                Automate Your{' '}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
                  Pet Business
                </span>{' '}
                with AI
              </h1>
              <p className="text-xl lg:text-2xl text-gray-300 leading-relaxed">
                Bookings. Upsells. Reminders. All on Autopilot.
              </p>
            </motion.div>

            <motion.div variants={fadeInUp} className="flex flex-col sm:flex-row gap-4">
              <motion.button
                whileHover={{ scale: 1.05, boxShadow: "0 0 30px rgba(0, 255, 194, 0.4)" }}
                whileTap={{ scale: 0.95 }}
                onClick={onGetStarted} 
                className="bg-primary text-dark px-8 py-4 rounded-xl text-lg font-semibold hover:bg-primary/90 transition-all duration-300 animate-glow"
              >
                Book Free Demo
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="border-2 border-secondary text-secondary px-8 py-4 rounded-xl text-lg font-semibold hover:bg-secondary hover:text-dark transition-all duration-300"
              >
                Watch Demo
              </motion.button>
            </motion.div>

            <motion.div variants={fadeInUp} className="flex items-center space-x-8 pt-4">
              <div className="flex items-center space-x-2">
                <CheckCircle className="w-5 h-5 text-primary" />
                <span className="text-gray-300">No Setup Required</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle className="w-5 h-5 text-primary" />
                <span className="text-gray-300">24/7 Support</span>
              </div>
            </motion.div>
          </div>

          <motion.div 
            variants={fadeInUp}
            className="relative flex justify-center"
          >
            <PetChatUI />
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
};

export default HeroSection;