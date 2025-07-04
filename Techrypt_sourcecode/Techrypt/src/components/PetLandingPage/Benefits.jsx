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
            <div className="bg-gradient-to-br from-dark-lighter to-dark-light rounded-3xl p-8 border border-dark-light shadow-2xl relative overflow-hidden">
              {/* Animated background elements */}
              <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-primary/10 to-secondary/10 rounded-full blur-3xl"></div>
              <div className="absolute bottom-0 left-0 w-24 h-24 bg-gradient-to-tr from-secondary/10 to-primary/10 rounded-full blur-2xl"></div>
              
              <div className="relative space-y-8">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-2xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">Live Analytics</h3>
                    <p className="text-sm text-gray-400 mt-1">Real-time performance metrics</p>
                  </div>
                  <div className="flex space-x-2">
                    <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                    <div className="w-3 h-3 bg-primary rounded-full opacity-50"></div>
                    <div className="w-3 h-3 bg-secondary rounded-full opacity-30"></div>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-dark rounded-xl p-6 hover:bg-dark-light transition-colors duration-300">
                    <div className="text-4xl font-bold text-primary mb-2">+247%</div>
                    <div className="text-sm text-gray-400">Lead Conversion</div>
                    <div className="text-xs text-green-400 mt-1">↗ +32% vs last month</div>
                  </div>
                  <div className="bg-dark rounded-xl p-6 hover:bg-dark-light transition-colors duration-300">
                    <div className="text-4xl font-bold text-secondary mb-2">24/7</div>
                    <div className="text-sm text-gray-400">Response Time</div>
                    <div className="text-xs text-blue-400 mt-1">Instant replies</div>
                  </div>
                </div>

                <div className="bg-dark rounded-xl p-6 hover:bg-dark-light transition-colors duration-300">
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-lg font-semibold text-gray-300">AI Performance</span>
                    <span className="text-sm text-primary bg-primary/20 px-3 py-1 rounded-full">97% Accuracy</span>
                  </div>
                  <div className="space-y-3">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-400">Response Quality</span>
                      <span className="text-green-400">Excellent</span>
                    </div>
                    <div className="w-full bg-dark-light rounded-full h-3">
                      <div className="bg-gradient-to-r from-primary to-secondary h-3 rounded-full w-[97%] shadow-lg shadow-primary/30"></div>
                    </div>
                    <div className="flex justify-between text-xs text-gray-500">
                      <span>Learning continuously</span>
                      <span>Real-time optimization</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Enhanced floating elements */}
            <div className="absolute -bottom-6 -right-6 w-32 h-32 bg-gradient-to-br from-primary/30 to-secondary/30 rounded-3xl opacity-60 animate-pulse blur-sm"></div>
            <div className="absolute -top-4 -left-4 w-20 h-20 bg-gradient-to-br from-secondary/20 to-primary/20 rounded-2xl opacity-40 animate-bounce"></div>
          </motion.div>
        </motion.div>
      </div>   
    </section>
  );
};

export default BenefitsSection;