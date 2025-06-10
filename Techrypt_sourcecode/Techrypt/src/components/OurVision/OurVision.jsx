import { motion } from "framer-motion";
import target from "../../assets/svgs/target.svg";
import rocket from "../../assets/svgs/rocket.svg";

export default function OurVision() {
  const container = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
        delayChildren: 0.3
      }
    }
  };

  const item = {
    hidden: { opacity: 0, x: 100 },
    visible: {
      opacity: 1,
      x: 0,
      transition: {
        type: "spring",
        stiffness: 100,
        damping: 10,
        duration: 0.8
      }
    }
  };

  const cards = [
    {
      icon: rocket,
      title: "Our Vision",
      bg: "bg-primary",
      textColor: "text-[#180830]",
      text: "To build a future where people master high-income digital skills and businesses thrive with next-gen technology."
    },
    {
      icon: target,
      title: "Our Philosophy",
      bg: "bg-primary",
      textColor: "text-[#180830]",
      text: "To deliver meaningful conversations across the entire brand experience."
    }
  ];

  return (
    <div className="bg-six  py-12 text-center overflow-x-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <motion.div
          className="flex flex-col md:flex-row items-center justify-center gap-6 md:gap-8 mt-10 md:mt-16"
          initial="hidden"
          whileInView="visible"
          viewport={{ margin: "-100px" }}
          variants={container}
        >
          {cards.map((card, index) => (
            <motion.div
              key={index}
              className={`${card.bg} w-full md:h-[450px] text-center shadow-lg relative rounded-[40px] flex flex-col gap-4 p-6`}
              variants={item}
              whileHover={{ scale: 1.02 }}
            >
              <div className="flex justify-center mb-4 h-[45%]">
                <img src={card.icon} alt={card.title} className="h-full object-contain" />
              </div>
              <h3 className={`bebas text-5xl font-normal mt-3 ${card.textColor}`}>
                {card.title}
              </h3>
              <p className="text-base md:text-2xl font-semibold mt-4 text-black px-6">
                {card.text}
              </p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </div>
  );
}