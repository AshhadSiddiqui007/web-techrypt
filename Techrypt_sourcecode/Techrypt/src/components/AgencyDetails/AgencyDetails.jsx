import React from "react";
import { motion } from "framer-motion";
import { techryptLogo } from "../../assets/mainImages";
import { Link } from "react-router-dom";

const fadeUpVariants = {
  hidden: { opacity: 0, y: 50 },
  visible: (i) => ({
    opacity: 1,
    y: 0,
    transition: {
      delay: i * 0.2,
      duration: 0.6,
      ease: "easeOut",
    },
  }),
};

const buttonVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      delay: 0.8, // Appears after the text animations
      duration: 0.6,
      ease: "easeOut",
    },
  },
};

const AgencyDetails = () => {
  const points = [
    "Bridging Education and Execution",
    "Empowering Skills and Services",
    "Strategies for Digital Growth",
  ];

  return (
    <div className="flex flex-col md:flex-row justify-center items-start relative gap-10 text-white py-4 h-full">
      <img
        src={techryptLogo}
        alt=""
        width={300}
        className="w-[300px] md:w-[400px]"
      />

      <div className="flex flex-col">
        <div className="flex flex-col gap-1">
          {points.map((text, i) => (
            <motion.span
              key={i}
              custom={i}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: false, amount: 0.5 }}
              variants={fadeUpVariants}
              className={`text-[22px] md:text-[40px] px-1 py-1 leading-tight`}
            >
              {text}
            </motion.span>
          ))}
        </div>
        
        <Link to="/about">
          <motion.button
            initial="hidden"
            whileInView="visible"
            viewport={{ once: false, amount: 0.5 }}
            variants={buttonVariants}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="mt-6 px-10 py-4 text-lg bg-[#C4D322] hover:bg-[#B3C01F] text-black font-semibold rounded-lg transition-colors duration-300 self-start"
          >
            Learn About our Innovative Team
          </motion.button>
        </Link>
      </div>
    </div>
  );
};

export default AgencyDetails;