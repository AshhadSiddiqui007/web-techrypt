import React from 'react';
import { motion } from 'framer-motion';
import { Shield, BarChart3, Users } from 'lucide-react';

const BenefitsSection = () => {
  const benefits = [
    {
      icon: Shield,
      title: "No Missed Calls",
      description: "Every inquiry gets an instant, professional response"
    },
    {
      icon: BarChart3,
      title: "More Bookings, Less Work",
      description: "AI handles 80% of booking conversations automatically"
    },
    {
      icon: Users,
      title: "Works Everywhere",
      description: "Website, WhatsApp, Instagram - one AI, all platforms"
    }
  ];

  return (
    <section id="benefits" className="py-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="grid lg:grid-cols-2 gap-16 items-center"
        >
          {/* First column content */}
          <div className="space-y-8">
            <div>
              <h2 className="text-4xl lg:text-5xl font-bold mb-6">
                More Bookings,{' '}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
                  Less Work
                </span>
              </h2>
              <p className="text-xl text-gray-300 leading-relaxed">
                Our AI doesn't just answer questions—it actively grows your business while you focus on what you do best.
              </p>
            </div>

            <div className="space-y-6">
              {benefits.map((benefit, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -30 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-start space-x-4"
                >
                  <div className="w-12 h-12 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center flex-shrink-0">
                    <benefit.icon className="w-6 h-6 text-dark" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2">{benefit.title}</h3>
                    <p className="text-gray-300">{benefit.description}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Second column content */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="relative"
          >
            <div className="bg-gradient-to-br from-dark-lighter to-dark-light rounded-3xl p-8 border border-dark-light shadow-2xl">
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-2xl font-bold">Dashboard Analytics</h3>
                  <div className="flex space-x-2">
                    <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                    <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-dark rounded-xl p-4">
                    <div className="text-3xl font-bold text-primary">+127%</div>
                    <div className="text-sm text-gray-400">Bookings This Month</div>
                  </div>
                  <div className="bg-dark rounded-xl p-4">
                    <div className="text-3xl font-bold text-secondary">$15,420</div>
                    <div className="text-sm text-gray-400">Revenue Generated</div>
                  </div>
                  <div className="bg-dark rounded-xl p-4">
                    <div className="text-3xl font-bold text-primary">24/7</div>
                    <div className="text-sm text-gray-400">AI Availability</div>
                  </div>
                  <div className="bg-dark rounded-xl p-4">
                    <div className="text-3xl font-bold text-secondary">98%</div>
                    <div className="text-sm text-gray-400">Customer Satisfaction</div>
                  </div>
                </div>

                <div className="bg-dark rounded-xl p-4">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-sm text-gray-400">AI Performance</span>
                    <span className="text-sm text-primary">Excellent</span>
                  </div>
                  <div className="w-full bg-dark-light rounded-full h-2">
                    <div className="bg-gradient-to-r from-primary to-secondary h-2 rounded-full w-4/5"></div>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="absolute -bottom-4 -right-4 w-24 h-24 bg-gradient-to-br from-primary to-secondary rounded-2xl opacity-20 animate-pulse"></div>
          </motion.div>
        </motion.div>
      </div>   
    </section>
  );
};

export default BenefitsSection;