import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, X } from 'lucide-react';

const ComparisonSection = () => {
  const comparisons = [
    ["24/7 AI Chatbot", true, false],
    ["Automated Lead Capture", true, false],
    ["Multi-Platform Integration", true, false],
    ["Real-Time Analytics", true, false],
    ["Smart Appointment Booking", true, true],
    ["Revenue Tracking", true, false]
  ];

  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 bg-dark-lighter/50">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl lg:text-5xl font-bold mb-6 text-white">
            Why Choose{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">Techrypt AI?</span>
          </h2>
          <p className="text-xl text-gray-300">
            See the difference smart automation makes for your business
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-gradient-to-br from-dark-lighter to-dark-light rounded-3xl overflow-hidden border border-dark-light shadow-2xl relative"
        >
          {/* Background decoration */}
          <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-primary/10 to-secondary/10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 left-0 w-24 h-24 bg-gradient-to-tr from-secondary/10 to-primary/10 rounded-full blur-2xl"></div>
          
          {/* Table Headers */}
          <div className="hidden sm:grid grid-cols-3 gap-0 relative z-10">
            <div className="p-6 border-r border-dark-light">
              <h3 className="text-xl font-bold text-center text-gray-300">Features</h3>
            </div>
            <div className="p-6 border-r border-dark-light bg-gradient-to-r from-primary/20 to-secondary/20 relative">
              <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-secondary/10"></div>
              <h3 className="text-xl font-bold text-center text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary relative z-10">
                ✨ Techrypt AI
              </h3>
            </div>
            <div className="p-6">
              <h3 className="text-xl font-bold text-center text-gray-500">Traditional Tools</h3>
            </div>
          </div>

          {comparisons.map(([feature, techrypt, traditional], index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.05 }}
              className="border-t border-dark-light hover:bg-gradient-to-r hover:from-primary/5 hover:to-secondary/5 transition-all duration-300 relative z-10"
            >
              {/* Mobile Layout */}
              <div className="block sm:hidden p-6 bg-gradient-to-r from-dark-lighter/50 to-dark-light/50">
                <div className="text-lg font-semibold mb-3 text-gray-200">{feature}</div>
                <div className="flex justify-between items-center">
                  <div className="flex items-center gap-3 bg-gradient-to-r from-primary/20 to-secondary/20 px-4 py-2 rounded-lg">
                    <span className="text-primary font-semibold">Techrypt AI:</span>
                    {techrypt ? (
                      <CheckCircle className="w-6 h-6 text-primary" />
                    ) : (
                      <X className="w-6 h-6 text-gray-500" />
                    )}
                  </div>
                  <div className="flex items-center gap-3 bg-dark-light/50 px-4 py-2 rounded-lg">
                    <span className="text-gray-400 font-medium">Traditional:</span>
                    {traditional ? (
                      <CheckCircle className="w-6 h-6 text-gray-400" />
                    ) : (
                      <X className="w-6 h-6 text-gray-500" />
                    )}
                  </div>
                </div>
              </div>

              {/* Desktop Layout */}
              <div className="hidden sm:grid grid-cols-3 gap-0">
                <div className="p-6 border-r border-dark-light">
                  <span className="font-semibold text-gray-200 text-lg">{feature}</span>
                </div>
                <div className="p-6 border-r border-dark-light bg-gradient-to-r from-primary/10 to-secondary/10 text-center relative">
                  <div className="absolute inset-0 bg-gradient-to-r from-primary/5 to-secondary/5"></div>
                  <div className="relative z-10">
                    {techrypt ? (
                      <div className="flex items-center justify-center">
                        <CheckCircle className="w-8 h-8 text-primary drop-shadow-lg" />
                      </div>
                    ) : (
                      <X className="w-8 h-8 text-gray-500 mx-auto" />
                    )}
                  </div>
                </div>
                <div className="p-6 text-center">
                  {traditional ? (
                    <CheckCircle className="w-8 h-8 text-gray-400 mx-auto" />
                  ) : (
                    <X className="w-8 h-8 text-gray-500 mx-auto opacity-60" />
                  )}
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};

export default ComparisonSection;
