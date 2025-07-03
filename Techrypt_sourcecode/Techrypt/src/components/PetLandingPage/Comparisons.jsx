import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, X } from 'lucide-react';

const ComparisonSection = () => {
  const comparisons = [
    ["24/7 AI Chatbot", true, false],
    ["Automated Upsells", true, false],
    ["50+ Languages", true, false],
    ["Real-Time Booking", true, true],
    ["WhatsApp Integration", true, false],
    ["Instagram DMs", true, false],
    ["Smart Reminders", true, true],
    ["Revenue Analytics", true, false]
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
          <h2 className="text-4xl lg:text-5xl font-bold mb-6">
            Techrypt AI vs{' '}
            <span className="text-gray-500">Traditional Software</span>
          </h2>
          <p className="text-xl text-gray-300">
            See why smart pet business owners are making the switch
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-gradient-to-br from-dark-lighter to-dark-light rounded-3xl overflow-hidden border border-dark-light"
        >
          {/* Table Headers */}
          <div className="hidden sm:grid grid-cols-3 gap-0">
            <div className="p-6 border-r border-dark-light">
              <h3 className="text-xl font-bold text-center">Features</h3>
            </div>
            <div className="p-6 border-r border-dark-light bg-primary/10">
              <h3 className="text-xl font-bold text-center text-primary">Techrypt AI</h3>
            </div>
            <div className="p-6">
              <h3 className="text-xl font-bold text-center text-gray-400">Traditional</h3>
            </div>
          </div>

          {comparisons.map(([feature, techrypt, traditional], index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.05 }}
              className="border-t border-dark-light hover:bg-dark-light/30 transition-colors"
            >
              {/* Mobile Layout */}
              <div className="block sm:hidden p-4">
                <div className="text-base font-semibold mb-2">{feature}</div>
                <div className="flex justify-between text-sm">
                  <div className="flex items-center gap-2">
                    <span className="text-primary font-medium">Techrypt AI:</span>
                    {techrypt ? (
                      <CheckCircle className="w-5 h-5 text-primary" />
                    ) : (
                      <X className="w-5 h-5 text-gray-500" />
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-gray-400 font-medium">Traditional:</span>
                    {traditional ? (
                      <CheckCircle className="w-5 h-5 text-gray-400" />
                    ) : (
                      <X className="w-5 h-5 text-gray-500" />
                    )}
                  </div>
                </div>
              </div>

              {/* Desktop Layout */}
              <div className="hidden sm:grid grid-cols-3 gap-0">
                <div className="p-4 border-r border-dark-light">
                  <span className="font-medium">{feature}</span>
                </div>
                <div className="p-4 border-r border-dark-light bg-primary/5 text-center">
                  {techrypt ? (
                    <CheckCircle className="w-6 h-6 text-primary mx-auto" />
                  ) : (
                    <X className="w-6 h-6 text-gray-500 mx-auto" />
                  )}
                </div>
                <div className="p-4 text-center">
                  {traditional ? (
                    <CheckCircle className="w-6 h-6 text-gray-400 mx-auto" />
                  ) : (
                    <X className="w-6 h-6 text-gray-500 mx-auto" />
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
