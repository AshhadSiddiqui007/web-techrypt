import { motion } from "framer-motion";
import bag from "../../assets/svgs/bag.svg";
import media from "../../assets/svgs/media.svg";
import starBadge from "../../assets/svgs/starBadge.svg";

export default function AboutCards() {
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

  const cards = [
    {
      icon: starBadge,
      title: "Performance",
      color: "text-blue-600",
      text: "We deliver measurable growth. Our strategies are rooted in results — from conversions to engagement to ROI."
    },
    {
      icon: media,
      title: "Creative",
      color: "text-red-500",
      text: "We blend design with data to create work that not only looks amazing but also moves the needle."
    },
    {
      icon: bag,
      title: "Work",
      color: "text-purple-500",
      text: "From training programs to client projects, every solution we deliver is tailored, tech-enabled, and future-ready."
    }
  ];

  return (
    <div className="md:py-12 text-center bg-black">
      <motion.div 
        className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true , margin: "-100px" }}
        variants={container}
      >
        <div className="md:py-20 px-5 grid grid-cols-1 md:grid-cols-3 gap-8">
          {cards.map((card, index) => (
            <motion.div
              key={index}
              className="relative border-2 border-primary rounded-xl p-3 md:p-16 bg-gray-900"
              variants={item}
              whileHover={{ scale: 1.05 }}
            >
              <div className="absolute -top-7 md:-top-12 left-1/2 transform -translate-x-1/2 bg-gray-900 rounded-full p-3 border-b-2 border-primary">
                <img src={card.icon} alt={card.title} className="h-9 md:h-12 w-9 md:w-12" />
              </div>
              <h3 className={`text-xl font-bold uppercase mt-8 mb-2 ${card.color}`}>
                {card.title}
              </h3>
              <p className="text-white text-sm md:text-base glowing-yellow">
                {card.text}
              </p>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}