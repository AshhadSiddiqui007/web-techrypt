import React, { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { BsArrowRight } from "react-icons/bs";
import { Link } from "react-router-dom";

const SectionComponent = ({ heading, text, bgImageSrc, imagePath, imageAlt, reverse }) => {
  const sectionRef = useRef(null);
  const [sectionHover, setSectionHover] = React.useState(false);
  const { scrollYProgress } = useScroll({
    target: sectionRef,
    offset: ["start end", "end start"],
  });

  const scale = useTransform(scrollYProgress, [0, 1], [0.9, 1.5]);

  // Split text into lines for animation
  const textLines = text.split('\n').filter(line => line.trim() !== '');

  // Animation variants
  const overlayVariants = {
    initial: { translate: 0 },
    hover: { translateY: "100%" }
  };

  const bgImageVariants = {
    initial: { scale: 1 },
    hover: { scale: 1.05 }
  };

  const textVariants = {
    hidden: {
      opacity: 0,
      x: reverse ? 100 : -100,
    },
    visible: {
      opacity: 1,
      x: 0,
      transition: {
        duration: 0.6,
        ease: "easeOut",
      },
    }
  };

  const lineVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: (i) => ({
      opacity: 1,
      y: 0,
      transition: {
        delay: i * 0.15,
        duration: 0.5,
        ease: "easeOut"
      }
    })
  };

  return (
    <section
      ref={sectionRef}
      className={`flex flex-col w-full md:w-[90%] mx-auto md:border-l-[1px] md:border-r-[1px] md:flex-row items-center justify-between gap-6 md:gap-10 px-4 md:px-20 py-12 md:py-24 text-white relative group overflow-hidden ${reverse ? "md:flex-row-reverse" : ""
        }`}
    >
      {/* Background Image Div (separate) */}
      <motion.div className="absolute inset-0 z-0">
        <img
          className="object-cover h-full w-full transition-all scale-125 ease-in duration-1000 group-hover:scale-100"
          src={bgImageSrc}
          alt=""
        />
      </motion.div>
      <div className="absolute inset-0 z-0 bg-black opacity-50" />
      {/* Black Overlay Div */}
      <motion.div
        className={`absolute inset-0 bg-black z-10 transition-all duration-300 group-hover:translate-y-full`}
        onMouseEnter={() => setSectionHover(true)}
        onMouseLeave={() => setSectionHover(false)}
        transition={{ duration: 0.5, ease: "easeOut" }}
      />

      <div className="flex flex-col md:flex-row justify-between items-start z-20 w-full gap-6 md:gap-8">
        <div className="flex flex-col items-start gap-3 md:gap-4 w-full md:w-1/3">
          <motion.h2
            className="text-responsive-2xl md:text-responsive-4xl font-bold leading-tight"
            variants={textVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: false, amount: 0.5 }}
          >
            {heading}
          </motion.h2>
          <motion.div
            className="text-3xl md:text-5xl text-primary touch-target"
            whileHover={{ x: 10 }}
            whileTap={{ scale: 0.95 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            <Link to={"/Work"} className="inline-block p-2">
              <BsArrowRight />
            </Link>
          </motion.div>
        </div>

        <motion.div
          className="w-full md:w-1/3 font-medium z-20 text-left"
          variants={textVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: false, amount: 0.5 }}
        >
          {textLines.map((line, i) => (
            <motion.p
              key={i}
              className="text-white text-responsive-sm md:text-responsive-lg leading-relaxed mb-2"
              custom={i}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: false, amount: 0.5 }}
              variants={lineVariants}
              transition={{ delay: i * 0.15, duration: 0.5, ease: "easeOut" }}
            >
              {line}
            </motion.p>
          ))}
        </motion.div>
      </div>

      {/* 
      <div className="w-full md:w-[50%] flex justify-center mt-10 md:mt-0 z-20">
        <motion.img
          src={imagePath}
          alt={imageAlt}
          className="w-[150px] sm:w-[200px] md:w-[250px] lg:w-[300px] rounded-[10px] drop-shadow-[0_0_10px_#F5FF1E] object-contain"
          style={{ scale }}
        />
      </div> */}
    </section>
  );
};

export default SectionComponent;