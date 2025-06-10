import React from "react";
import { motion } from "framer-motion";

export default function Design() {
  return (
    <motion.div
      className="bg-black py-5 px-4 sm:px-36 flex flex-col items-center gap-5"
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.8 }}
    >
      {/* Heading */}
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        whileInView={{ scale: 1, opacity: 1 }}
        viewport={{ once: true }}
        transition={{ type: "spring", stiffness: 100 }}
      >
        <h3 className="text-white text-xl sm:text-2xl font-medium border-2 border-white rounded-2xl px-3 py-1 text-center">
          MIRO
        </h3>
      </motion.div>

      {/* Paragraph */}
      <motion.div
        initial={{ y: 30, opacity: 0 }}
        whileInView={{ y: 0, opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="max-w-4xl"
      >
        <p className="text-white text-3xl sm:text-5xl font-medium text-center leading-tight sm:leading-[54px]">
          has been an invaluable partner in managing and scaling Miro's influencer marketing program. Their team consistently creates tailored, data-driven strategies that align with our goals and deliver impressive ROI.

        </p>
      </motion.div>

      {/* Button */}
      <motion.div
        initial={{ y: 30, opacity: 0 }}
        whileInView={{ y: 0, opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6, delay: 0.4 }}
      >
        <button className="bg-primary glow-hover  text-white border-none px-8 py-5 text-xl font-bold rounded-full  transition-all duration-300 mb-5">
          Get Started
        </button>
      </motion.div>
    </motion.div>
  );
}