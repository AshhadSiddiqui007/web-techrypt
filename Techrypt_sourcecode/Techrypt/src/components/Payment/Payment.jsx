import React from "react";
import { motion } from "framer-motion";

export default function Payment() {
  const container = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.3
      }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        type: "spring",
        stiffness: 100,
        damping: 10
      }
    }
  };

  const paymentMethods = [
    "Credit/Debit Cards",
    "Bank Transfers",
    "Mobile Payments (e.g., Apple Pay, Google Pay)"
  ];

  const industries = [
    "High School Advertising",
    "Healthcare",
    "E-commerce",
    "Real Estate",
    "Education",
    "Fitness",
    "Beauty",
     "Automotive",
    "Professional Services"
   
  ];

  return (
    <motion.div 
      className="bg-black flex flex-col md:flex-row justify-center gap-5 md:gap-8 p-4 md:p-8"
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true }}
      variants={container}
    >
      {/* Left Column - Payment Options */}
      <motion.div 
        className="flex flex-col gap-4 flex-1 max-w-[500px]"
        variants={item}
      >
        <motion.h1 
          className="text-3xl md:text-4xl font-medium leading-tight text-white glowing-green text-left md:text-left"
          variants={item}
        >
          Payment Options
        </motion.h1>
        
        <motion.p 
          className="text-lg md:text-xl font-light leading-snug text-white border-t-2 border-white pt-3 text-left md:text-left"
          variants={item}
        >
          We offer a variety of payment methods to suit your needs:
        </motion.p>
        
        <motion.ul 
          className="flex flex-col gap-3 list-none"
          variants={container}
        >
          {paymentMethods.map((method, index) => (
            <motion.li 
              key={index}
              className="text-lg md:text-xl font-light leading-snug text-white border-t-2 border-white pt-3 text-left md:text-left"
              variants={item}
            >
              {method}
            </motion.li>
          ))}
        </motion.ul>
        
        <motion.p 
          className="text-lg md:text-xl font-light leading-snug text-white text-left md:text-left"
          variants={item}
        >
          Secure and flexible options for all customers!
        </motion.p>
      </motion.div>

      {/* Right Column - Industries */}
      <motion.div 
        className="flex flex-col gap-4 flex-1 max-w-[500px]"
        variants={item}
      >
        <motion.h1 
          className="text-3xl md:text-4xl font-medium leading-tight text-white glowing-green text-left md:text-left"
          variants={item}
        >
          Industries
        </motion.h1>
        
        <motion.div 
          className="flex flex-col gap-3"
          variants={container}
        >
          {industries.map((industry, index) => (
            <motion.p 
              key={index}
              className="text-lg md:text-xl font-light leading-snug text-white border-t-2 border-white pt-3 text-left md:text-left"
              variants={item}
            >
              {industry}
            </motion.p>
          ))}
        </motion.div>
      </motion.div>
    </motion.div>
  );
}