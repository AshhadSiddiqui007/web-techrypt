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
              Through thoughtful design, smart technology, and strategic marketing, we build digital brand journeys that elevate your presence and accelerate your success
            </h2>
          </motion.div>

        {/* Separator - now animating height */}
          <motion.div
            className="w-px mx-auto bg-pink-500 glow-pink"
            initial={{ height: 0 }}
            whileInView={{ height: "200px" }}
            viewport={{ once: false }}
            transition={{ duration: 0.8, delay: 0.6, ease: "easeOut" }}
          />


          {/* Bordered Paragraph */}
          <motion.div
            className="border-3 border-pink-500 rounded-lg p-6 glow-pink pb-10"
            initial={{ scale: 0.95, opacity: 0 }}
            whileInView={{ scale: 1, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.4 }}
            whileHover={{ scale: 1.02 }}
          >
            <h3 className="text-l md:text-2xl font-bold  text-white text-center pb-25">
                Your Growth, Automated<br></br>
                Powered by AI. Driven by Data.<br></br><br></br>
            </h3>
            <h2 className="text-l md:text-xl  text-white text-center">
                Techrypt transforms how you build and grow online. Our AI doesn’t just create your website—it evolves it, using real-time data to optimize for performance, engagement, and revenue through embedded systems.
            </h2>
          </motion.div>

          {/* Regular Paragraph */}
          <motion.div
            className="w-full"
            initial={{ y: 20, opacity: 0 }}
            whileInView={{ y: 0, opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.8 }}
          >
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
}