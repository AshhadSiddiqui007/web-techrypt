import React from "react";
import { motion } from "framer-motion";

export default function AboutPara() {
  return (
    <div className="w-full py-16 px-4 sm:px-6 lg:px-8 bg-black">
      <motion.div
        className="max-w-6xl mx-auto"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true, margin: "-100px" }}
        transition={{ duration: 0.8 }}
      >
        <div className="flex flex-col gap-8">
          {/* Heading Paragraph */}
          <motion.div
            className="w-full"
            initial={{ y: 20, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <h2 className="text-2xl md:text-3xl text-center lg:text-4xl font-medium text-white">
              Techrypt.io is a forward-thinking team on a mission to revolutionize how individuals learn and how businesses grow. By combining real-world experience with digital innovation, we empower our clients to build, automate, and scale using advanced tools in AI, design, development, and marketing.
            </h2>
          </motion.div>

          {/* Bordered Paragraph */}
          <motion.div
            className="border-2 border-pink-500 rounded-lg p-6 glow-pink"
            initial={{ scale: 0.95, opacity: 0 }}
            whileInView={{ scale: 1, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.4 }}
            whileHover={{ scale: 1.02 }}
          >
            <h3 className="text-xl md:text-2xl font-bold  text-white text-center">
              At Techrypt, we treat our clients as our partners.
            </h3>
          </motion.div>

          {/* Separator - now animating height */}
          <motion.div
            className="w-px mx-auto bg-pink-500 glow-pink"
            initial={{ height: 0 }}
            whileInView={{ height: "200px" }}
            viewport={{ once: false }}
            transition={{ duration: 0.8, delay: 0.6, ease: "easeOut" }}
          />

          {/* Regular Paragraph */}
          <motion.div
            className="w-full"
            initial={{ y: 20, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.8 }}
          >
            <p className="text-lg md:text-xl text-center text-gray-300 md: px-14">
              We offer scalable services for businesses and skill-building programs for individuals — helping both move faster, smarter, and stronger in the digital world.

            </p>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
}