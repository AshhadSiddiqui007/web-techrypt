import React from "react";
import { motion } from "framer-motion";
import mask1 from "../../assets/svgs/mask1.svg"
import mask2 from "../../assets/svgs/mask2.svg"
import mask3 from "../../assets/svgs/mask3.svg"
import mask4 from "../../assets/svgs/mask4.svg"
import mask5 from "../../assets/svgs/mask5.svg"
import VerticlesCard from "../VerticlesCard/VerticlesCard";
export default function Verticals() {
  const verticals = [
    { text: "E-commerce", class: mask1 },
    { text: "Education", class: mask3 },
     { text: "Fashion", class: mask2 },
    { text: "Travel", class: mask4 },
    { text: "Finance", class: mask5 },
    { text: "Pet Industry", class: mask2 },
    { text: "Health", class: mask3 },
    { text: "Entertainment", class: mask5 },
    { text: "Don't see your industry?", class: mask2 },
  ];

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
    hidden: { opacity: 0, scale: 0.8 },
    visible: {
      opacity: 1,
      scale: 1,
      transition: {
        type: "spring",
        stiffness: 100,
        damping: 10
      }
    }
  };
  const cardAnimation = {
    hidden: { opacity: 0, scale: 0.8, y: 20 },
    visible: {
      opacity: 1,
      scale: 1,
      y: 0,
      transition: {
        type: "spring",
        stiffness: 100,
        damping: 10,
        duration: 0.6
      }
    }
  };
  return (
    <div className="bg-black flex flex-col items-center justify-center min-h-screen pt-10 overflow-hidden">
      <motion.h1
        className="text-white text-5xl md:text-6xl font-bold text-center mb-12"
        initial={{ opacity: 0, y: -20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.8 }}
      >
        Our Vertices
      </motion.h1>
      <div className="flex gap-6 flex-wrap max-md:flex-col justify-center w-full px-5 py-4">
        {verticals.map((itemData, i) => (

          <VerticlesCard foldSize={50} className="w-full md:w-[32%] bg-[#D8E35A] bg-opacity-30 text-center" >
            <motion.div

              initial="hidden"
              whileInView="visible"
              viewport={{ once: false, }}
              variants={cardAnimation}
              whileHover={{ scale: 1.05 }}
            >
              <h1 className="w-full flex justify-center items-center p-5 text-xl md:text-5xl md:h-48 lg:h-52 text-primary  font-semibold cursor-default border-2 border-primary rounded-xl">
                {itemData.text.toUpperCase()}</h1>
            </motion.div>
            <div className="h-3 w-3 rounded-full bg-primary absolute top-4 left-4"></div>

          </VerticlesCard>
        ))}
      </div>

    </div>
  );
}