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
      className={`flex flex-col md:w-[90%] mx-auto md:border-l-[1px] md:border-r-[1px] md:flex-row items-center justify-between gap-10 px-5 md:px-20  py-24 text-white relative group overflow-hidden ${reverse ? "md:flex-row-reverse" : ""
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

      <div className="flex md:flex-row flex-col justify-between z-20 w-full">
        <div className="flex flex-col items-start gap-2 w-full md:w-1/3">
          <motion.h2
            className="text-[28px] sm:text-[35px] md:text-[45px] font-bold leading-[110%]"
            variants={textVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: false, amount: 0.5 }}
          >
            {heading}
          </motion.h2>
          <motion.div
            className="text-5xl text-primary"
            whileHover={{ x: 10 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            <Link to={"/Work"}><BsArrowRight /></Link>
          </motion.div>
        </div>

        <motion.div
          className="max-w-full md:w-1/3 font-semibold z-20 md:text-left"
          variants={textVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: false, amount: 0.5 }}
        >
          {textLines.map((line, i) => (
            <motion.p
              key={i}
              className="text-white text-[14px] sm:text-[15px] md:text-[20px] leading-relaxed"
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