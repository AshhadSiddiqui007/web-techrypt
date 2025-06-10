import React, { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import gif from "../../assets/gifs/text_2.gif";

export default function Slider() {
  const slides = [
    {
      title: "This is our way",
      content: `Our passion is to tell stories and create ideas in all shapes, sizes and worlds. We bring ideas to life through impactful creative work across all communication touchpoints.`,
    },
    {
      title: "This is another way",
      content: `We strive to create powerful connections and innovate across various domains.`,
    },
    {
      title: "This is the future",
      content: `Our goal is to create memorable experiences that transcend traditional mediums.`,
    },
  ];

  const containerRef = useRef(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end end"]
  });

  // Horizontal scroll animation
  const x = useTransform(scrollYProgress, [0, 1], ["0%", `-${(slides.length - 1) * 100}%`]);

  return (
    <>
      {/* Desktop - Horizontal Scroll Section */}
      <section
        ref={containerRef}
        className="relative h-[300vh] hidden md:block"
      >
        <div className="sticky top-0 h-screen w-full overflow-hidden bg-black">
          <motion.div
            className="flex h-full w-full"
            style={{ x }}
          >
            {slides.map((slide, index) => (
              <div
                key={index}
                className="flex-shrink-0 w-full h-full flex flex-col items-center justify-center px-4"
              >
                <motion.h1
                  className="text-white glowing-green text-6xl md:text-8xl font-medium font-['Right_Grotesk'] leading-[5.6rem] tracking-tight mb-12"
                  initial={{ opacity: 0, y: 50 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: 0.2 }}
                >
                  {slide.title}
                </motion.h1>
                <motion.h3
                  className="text-white text-center text-2xl md:text-4xl leading-[3.4rem] tracking-tight font-['Right_Grotesk'] max-w-4xl md:px-10"
                  initial={{ opacity: 0, y: 50 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: 0.4 }}
                >
                  {/* {slide.content.split(" ").slice(0, 6).join(" ")}
                  <img
                    className="inline-block w-16 md:w-20 wh7 md:h-9 mx-1 mb-1 object-cover rounded-full"
                    src={gif}
                    alt="Animated text"
                  />
                  {slide.content.split(" ").slice(6).join(" ")} */}
                  {slide.content}
                </motion.h3>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Mobile - Vertical Stack */}
      <div className="md:hidden flex flex-col gap-10 py-10 px-2 bg-black">
        {slides.map((slide, index) => (
          <div key={index} className="flex flex-col gap-3 items-center h-fit">
            <motion.h1
              className="text-white glowing-green text-4xl font-medium font-['Right_Grotesk']"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4 }}
            >
              {slide.title}
            </motion.h1>
            <motion.h3
              className="text-white text-center text-xl"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: 0.2 }}
            >
              {slide.content}
            </motion.h3>
          </div>
        ))}
      </div>
    </>
  );
}