import React from 'react';
import { motion } from 'framer-motion';
import { MessageCircle, Calendar, Globe } from 'lucide-react';

const WhyLoveUs = ({ fadeInUp, staggerContainer }) => {
  const features = [
    {
      icon: MessageCircle,
      title: "24/7 AI Chatbot",
      description: "Never miss a customer inquiry. Our AI responds instantly, books appointments, and answers questions around the clock."
    },
    {
      icon: Calendar,
      title: "Automated Booking System",
      description: "Smart scheduling that prevents double-bookings, sends reminders, and optimizes your calendar for maximum revenue."
    },
    {
      icon: Globe,
      title: "Multilingual Client Support",
      description: "Serve customers in their preferred language. Our AI speaks 50+ languages fluently and culturally adapts responses."
    }
  ];

  return (
    <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-dark-lighter/50">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl lg:text-5xl font-bold mb-6">
            Why Pet Businesses{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
              Love Us
            </span>
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Transform your pet grooming business with AI that never sleeps, never forgets, and always upsells.
          </p>
        </motion.div>

        <motion.div
          variants={staggerContainer}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true }}
          className="grid md:grid-cols-3 gap-8"
        >
          {features.map((feature, index) => (
            <motion.div
              key={index}
              variants={fadeInUp}
              whileHover={{ y: -10, transition: { duration: 0.3 } }}
              className="bg-gradient-to-br from-dark-lighter to-dark-light rounded-2xl p-8 border border-dark-light hover:border-primary/50 transition-all duration-300 group"
            >
              <div className="w-16 h-16 bg-gradient-to-br from-primary to-secondary rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <feature.icon className="w-8 h-8 text-dark" />
              </div>
              <h3 className="text-2xl font-bold mb-4 group-hover:text-primary transition-colors">
                {feature.title}
              </h3>
              <p className="text-gray-300 leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};

export default WhyLoveUs;