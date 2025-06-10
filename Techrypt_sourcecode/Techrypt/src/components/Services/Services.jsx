import React from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";

export default function Services() {
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
    hidden: { opacity: 0, y: 30 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        type: "spring",
        stiffness: 100,
        damping: 10,
        duration: 0.8
      }
    }
  };

  const rows = [
    [
      { text: "UGC Marketing", width: "w-auto" },
      { text: "Landing pages", width: "w-auto" },
      { text: "TikTok Marketing", width: "w-[198px]" }
    ],
    [
      { text: "TikTok Shop Management", width: "w-[266px]" },
      { text: "Performance Creative Design", width: "w-[266px]" },
      { text: "User Acquisition Strategy", width: "w-[266px]" }
    ],
    [
      { text: "Paid Media Campaigns", width: "w-[266px]" },
      { text: "Market Overview & Competitive Analysis", width: "w-[266px]" },
      { text: "  Panel Recruitment", width: "w-[266px]" }
    ]
  ];

  const getBorderRadius = (index) => {
    if (index === 1) return "rounded-[100px]"; // middle box
    return "rounded-[50px]"; // first and third boxes
  };

  return (
    <div className="bg-black py-16 px-4 sm:px-8 md:px-36 flex flex-col gap-3">
      <motion.h1
        className="text-4xl md:text-6xl font-bold text-center text-white leading-tight md:leading-[89px]"
        initial={{ opacity: 0, y: -20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
      >
        We deliver high-quality services tailored to your industry.
      </motion.h1>

      <motion.div
        className="mt-8 flex flex-col items-center gap-5"
        initial="hidden"
        whileInView="visible"
        viewport={{ margin: "-100px" }}
        variants={container}
      >
        {rows.map((row, rowIndex) => (
          <motion.div
            key={rowIndex}
            className="flex flex-col w-full md:flex-row gap-5 glowing-green"
            variants={container}
          >
            {row.map((box, boxIndex) => (
              <Link to={"/Contact"}>
                <motion.div
                  key={boxIndex}
                  className={`h-[150px] flex border-[3px] p-3 cursor-default border-white ${getBorderRadius(boxIndex)} w-full md:w-[363px] items-center justify-center  text-white bg-primary ${box.width}`}
                  variants={item}
                  whileHover={{ scale: 1.05 }}
                >

                  <p className=" text-xl md:text-2xl  text-center">
                    {box.text}
                  </p>
                </motion.div>
              </Link>

            ))}
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}