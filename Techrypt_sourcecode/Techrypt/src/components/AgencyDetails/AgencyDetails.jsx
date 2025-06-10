import React from "react";
import { motion } from "framer-motion";
import { techryptLogo } from "../../assets/mainImages";

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

const AgencyDetails = () => {
  const points = [
    "Bridging Education and Execution",
    "Empowering Skills and Services",
    "Strategies for Digital Growth",
  ];

  return (
    <div className="flex flex-col md:flex-row justify-center items-center relative gap-10 text-white  py-16  h-full">
      <img
        src={techryptLogo}
        alt=""
        width={300}
        className="w-[300px] md:w-[400px]"
      />

      <div className="flex flex-col gap-4">
        {points.map((text, i) => (
          <motion.span
            key={i}
            custom={i}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: false, amount: 0.5 }}
            variants={fadeUpVariants}
            className={`text-[22px] md:text-[40px] px-2 py-2 `}
          >
            {text}
          </motion.span>
        ))}
      </div>
    </div>
  );
};

export default AgencyDetails;
