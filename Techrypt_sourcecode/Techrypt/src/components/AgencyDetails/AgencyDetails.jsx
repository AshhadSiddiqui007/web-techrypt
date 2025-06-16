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
    <div className="container-responsive">
      <div className="flex flex-col md:flex-row justify-center items-center md:items-start relative gap-6 md:gap-10 text-white py-8 md:py-12 h-full">
        <div className="flex-shrink-0">
          <img
            src={techryptLogo}
            alt="Techrypt Logo"
            className="w-64 md:w-80 lg:w-96 h-auto object-contain mx-auto"
          />
        </div>

        <div className="flex flex-col text-center md:text-left max-w-lg">
          <div className="flex flex-col gap-2 md:gap-3">
            {points.map((text, i) => (
              <motion.span
                key={i}
                custom={i}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: false, amount: 0.5 }}
                variants={fadeUpVariants}
                className="text-responsive-lg md:text-responsive-3xl lg:text-4xl px-2 py-1 leading-tight font-semibold"
              >
                {text}
              </motion.span>
            ))}
          </div>

          <Link to="/about" className="self-center md:self-start mt-6 md:mt-8">
            <motion.button
              initial="hidden"
              whileInView="visible"
              viewport={{ once: false, amount: 0.5 }}
              variants={buttonVariants}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="btn-responsive bg-primary hover:bg-primary/90 text-black font-semibold rounded-lg transition-all duration-300 touch-target shadow-lg hover:shadow-xl"
            >
              Learn About our Innovative Team
            </motion.button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default AgencyDetails;