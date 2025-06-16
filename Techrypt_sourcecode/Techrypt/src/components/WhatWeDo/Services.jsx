import React, { useRef } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';
import "../../App.css";
import logos from '../../assets/logo/logos';
import { bgPattern } from '../../assets/mainImages';

const Services = ({className}) => {
    const CardContent = [
        {
            title: 'AI-Powered Scheduling Systems',
            img: logos.image1,
            content: '24/7 calendar filling with qualified leads'
        },
        {
            title: 'Social Media Automation',
            img: logos.image7,
            content: 'Hands-free content creation & scheduling'
        },
        {
            title: 'Meta Ads Funnels',
            img: logos.image3,
            content: 'Facebook & Instagram campaigns that convert.'
        },
        {
            title: 'Chatbot Setup',
            img: logos.image4,
            content: "AI-powered assistants that qualify leads and book appointments"
        },
        {
            title: 'Website + Funnel',
            img: logos.image4,
            content: "Conversion-optimized landing pages & sites"
        },
        {
            title: 'Branding & Automation',
            img: logos.image4,
            content: "Partner with us to build, scale, and lead in the digital age."
        },
    ];

    const containerRef = useRef(null);
    const { scrollYProgress } = useScroll({
        target: containerRef,
        offset: ["start end", "end start"]
    });

    const bgY = useTransform(scrollYProgress, [0, 1], ['20%', '0%']);
    const bgX = useTransform(scrollYProgress, [0, 1], ['20%', '0%']);
    const bgOpacity = useTransform(scrollYProgress, [0, 0.5, 1], [0.7, 1, 1]);

    const cardVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: (i) => ({
            opacity: 1,
            y: 0,
            transition: {
                delay: i * 0.1,
                duration: 0.5
            }
        })
    };

    return (
        <section
            ref={containerRef}
            className={`w-full h-auto relative overflow-hidden py-12 md:py-20 ${className}`}
        >
            {/* Background with zoom effect */}
            <motion.div
                className="absolute inset-0 bg-cover bg-center z-10"
                style={{
                    backgroundImage: `url(${bgPattern})`,
                    scale: 1.3,
                    x: bgX,
                    y: bgY,
                }}
            />

            <div className="container-responsive relative z-20">
                <motion.h1
                    className="text-white text-responsive-3xl md:text-responsive-5xl font-bold text-center mb-8 md:mb-12"
                    initial={{ opacity: 0, y: -20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.8 }}
                >
                    Our Services
                </motion.h1>

                <div className="w-11/12 mx-auto grid gap-12 md:gap-16 grid-cols-1 md:grid-cols-3">
                    {CardContent.map((content, index) => (
                        <motion.div
                            key={index}
                            className="bg-[#AEBB1E] text-white w-full h-45 lg:h-55 rounded-2xl p-8 glow-green service-card-responsive"
                            custom={index}
                            initial="hidden"
                            whileInView="visible"
                            viewport={{ once:false, margin: "-50px" }}
                            variants={cardVariants}
                        >
                            <div className="w-full h-20 flex justify-center items-center service-icon-container">
                                <img src={content.img} alt="" className="max-h-full service-icon" />
                            </div>
                            <h2 className="font-['Bebas_Neue'] text-xl md:text-2xl lg:text-3xl text-center mt-2 mb-2 service-title">
                                {content.title}
                            </h2>
                            <p className="font-['Inter'] text-center text-sm md:text-base service-description">
                                {content.content}
                            </p>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default Services;
