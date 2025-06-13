import React, { useState } from "react";
import { motion } from "framer-motion";
import { FaCircleArrowDown, FaCircleArrowUp } from "react-icons/fa6";
import { useNavigate } from "react-router-dom"; // Import useNavigate

export default function Content() {
  const [expanded, setExpanded] = useState(false);
  const navigate = useNavigate(); // Initialize useNavigate

  const handleOurWorkClick = () => {
    navigate('/work'); // Navigate to the /work page
  };

  return (
    <div className="bg-[#0f0f0f] px-4 py-10 sm:px-36 flex flex-col gap-5">
      {/* Work Section */}
      <motion.div
        className="flex flex-col items-center gap-3"
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
      >
        <motion.h1
          className="text-4xl sm:text-8xl font-normal text-white glowing-green font-['Right_Grotesk']"
          initial={{ scale: 0.9 }}
          whileInView={{ scale: 1 }}
          viewport={{ once: true }}
          transition={{ type: "spring", stiffness: 100 }}
        >
          How we do it
        </motion.h1>
        <motion.button
          className="bg-primary text-white border-none px-8 py-5 text-xl font-bold rounded-full glow-hover transition-colors duration-300"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleOurWorkClick} // Added onClick handler
        >
          Our Work
        </motion.button>
      </motion.div>

      {/* Vertical Line */}
      <motion.div
        className="w-0.5 bg-white h-40 mx-auto glowing-pink"
        initial={{ height: 0 }}
        whileInView={{ height: 160 }}
        transition={{ duration: 0.8 , delay: 0.3 }}
      />

      {/* Delivery Section */}
      <motion.div
        className="flex flex-col items-center text-center text-white gap-5 mb-16"
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6, delay: 0.2 }}
      >
        <motion.h1
          className="text-4xl sm:text-8xl font-normal glowing-green font-['Right_Grotesk']"
          initial={{ scale: 0.9 }}
          whileInView={{ scale: 1 }}
          viewport={{ once: true }}
          transition={{ type: "spring", stiffness: 100, delay: 0.2 }}
        >
          Delivery
        </motion.h1>
        <motion.p
          className="text-xl sm:text-5xl font-medium leading-tight"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          Using an end-to-end content creation and production solution, we
          ensure not only flawless execution but also delivery through the
          ecosystem of our agency
        </motion.p>
      </motion.div>


    </div>
  );
}
