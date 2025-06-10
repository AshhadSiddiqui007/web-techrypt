import React from "react";
import { motion } from "framer-motion";

export default function Awards() {
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
        damping: 10,
        duration: 0.8
      }
    }
  };

  const awards = [
    {
      column: 1,
      items: ["Feature"]
    },
    {
      column: 2,
      items: ["Immigration Consultancy Automation", "Student Counseling Automation", "Shopify Chatbot Integration"]
    },
    {
      column: 3,
      items: ["Customer Support", "Social Media Automation", "Sales Funnel", "Branding"]
    }
  ];

  return (
    <div className="min-h-[80vh] bg-black flex justify-center items-center p-5">
      <motion.div
        className="w-[85vw] min-h-[40vh] bg-primary rounded-2xl relative shadow-lg p-5 glowing-green"
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        whileHover={{
          y: -10,
          boxShadow: "0 12px 30px rgba(0, 0, 0, 0.25)"
        }}
      >
        <motion.div
          className="grid grid-cols-1 md:grid-cols-3 gap-8 p-8 h-auto"
          variants={container}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
        >
          {awards.map((column, colIndex) => (
            <motion.div 
              key={colIndex}
              className="flex flex-col"
              variants={container}
            >
              {column.items.map((award, index) => (
                <motion.div
                  key={index}
                  variants={item}
                >
                  <motion.h2
                    className="font-['Right_Grotesk'] font-medium text-xl md:text-2xl leading-7 tracking-wider text-white mb-2 hover:text-black  transition-colors cursor-default duration-300"
                    whileHover={{ scale: 1.05 }}
                  >
                    {award}
                  </motion.h2>
                  {index < column.items.length - 1 && (
                    <hr className="border border-white my-2" />
                  )}
                </motion.div>
              ))}
            </motion.div>
          ))}
        </motion.div>
      </motion.div>
    </div>
  );
}