import React from 'react';
import { motion } from 'framer-motion';
import { ChevronDown, ChevronUp } from 'lucide-react';

const FAQSection = ({ activeAccordion, toggleAccordion, fadeInUp, staggerContainer }) => {
  const faqs = [
    {
      question: "How quickly can I set up Techrypt AI?",
      answer: "Setup takes less than 15 minutes. We provide a simple embed code for your website and connect your existing booking system. No technical expertise required!"
    },
    {
      question: "Does it integrate with my current booking software?",
      answer: "Yes! Techrypt AI integrates with all major pet grooming software including PetExec, Groomer.io, and others through our API connections."
    },
    {
      question: "What if the AI can't answer a customer's question?",
      answer: "Our AI is trained specifically for pet grooming businesses, but if it encounters something unusual, it seamlessly transfers the conversation to you with full context."
    },
    {
      question: "How much does it cost?",
      answer: "We offer flexible pricing starting at $97/month with no setup fees. Most businesses see ROI within the first month through increased bookings."
    },
    {
      question: "Can I customize the AI's responses?",
      answer: "Absolutely! You can customize pricing, services, policies, and even the AI's personality to match your brand voice perfectly."
    }
  ];

  return (
    <section id="faq" className="py-20 px-4 sm:px-6 lg:px-8 bg-dark-lighter/50">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl lg:text-5xl font-bold mb-6">
            Frequently Asked{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
              Questions
            </span>
          </h2>
          <p className="text-xl text-gray-300">
            Everything you need to know about Techrypt AI
          </p>
        </motion.div>

        <motion.div
          variants={staggerContainer}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true }}
          className="space-y-4"
        >
          {faqs.map((faq, index) => (
            <motion.div
              key={index}
              variants={fadeInUp}
              className="bg-gradient-to-br from-dark-lighter to-dark-light rounded-2xl border border-dark-light overflow-hidden"
            >
              <button
                className="w-full p-6 text-left flex items-center justify-between hover:bg-dark-light/30 transition-colors"
                onClick={() => toggleAccordion(index)}
              >
                <span className="text-lg font-semibold">{faq.question}</span>
                {activeAccordion === index ? (
                  <ChevronUp className="w-6 h-6 text-primary" />
                ) : (
                  <ChevronDown className="w-6 h-6 text-gray-400" />
                )}
              </button>
              
              <motion.div
                initial={false}
                animate={{
                  height: activeAccordion === index ? "auto" : 0,
                  opacity: activeAccordion === index ? 1 : 0
                }}
                transition={{ duration: 0.3, ease: "easeInOut" }}
                className="overflow-hidden"
              >
                <div className="p-6 pt-0 text-gray-300 leading-relaxed">
                  {faq.answer}
                </div>
              </motion.div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};

export default FAQSection;