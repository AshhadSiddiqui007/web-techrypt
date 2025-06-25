import React from 'react';
import { motion } from 'framer-motion';

const CTASection = ({ openBookingModal }) => {
  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto text-center">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="space-y-8"
        >
          <h2 className="text-4xl lg:text-6xl font-bold">
            Start Automating{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
              Today
            </span>
          </h2>
          
          <p className="text-xl lg:text-2xl text-gray-300 max-w-2xl mx-auto">
            Join hundreds of pet businesses already using AI to grow their revenue while reducing workload
          </p>

          <motion.div className="flex flex-col sm:flex-row gap-4 justify-center">
            <motion.button
              whileHover={{ scale: 1.05, boxShadow: "0 0 40px rgba(0, 255, 194, 0.5)" }}
              whileTap={{ scale: 0.95 }}
              onClick={openBookingModal}
              className="bg-primary text-dark px-10 py-5 rounded-xl text-xl font-bold hover:bg-primary/90 transition-all duration-300 animate-glow"
            >
              Get Started for Free
            </motion.button>
            
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={openBookingModal}
              className="border-2 border-secondary text-secondary px-10 py-5 rounded-xl text-xl font-bold hover:bg-secondary hover:text-dark transition-all duration-300"
            >
              Schedule Demo
            </motion.button>
          </motion.div>

          <p className="text-gray-400">
            No credit card required • 14-day free trial • Cancel anytime
          </p>
        </motion.div>
      </div>
    </section>
  );
};

export default CTASection;