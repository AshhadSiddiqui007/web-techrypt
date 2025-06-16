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

                <div className="grid gap-6 md:gap-8 lg:gap-12 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
                    {CardContent.map((content, index) => (
                        <motion.div
                            key={index}
                            className="bg-primary/65 text-white w-full rounded-2xl glow-green shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                            style={{
                                minHeight: 'clamp(280px, 35vh, 400px)', /* Proportional height scaling */
                                padding: 'clamp(1.5rem, 4vw, 2.5rem)' /* Proportional padding */
                            }}
                            custom={index}
                            initial="hidden"
                            whileInView="visible"
                            viewport={{ once: false, margin: "-50px" }}
                            variants={cardVariants}
                            whileHover={{ y: -5 }}
                        >
                            <div
                                className="w-full flex justify-center items-center mb-4"
                                style={{ height: 'clamp(60px, 8vh, 100px)' }} /* Proportional icon area */
                            >
                                <img
                                    src={content.img}
                                    alt={content.title}
                                    className="object-contain"
                                    style={{
                                        maxHeight: '100%',
                                        width: 'auto',
                                        maxWidth: 'clamp(50px, 8vw, 80px)' /* Proportional icon size */
                                    }}
                                />
                            </div>
                            <h2
                                className="font-['Bebas_Neue'] text-center mb-3 md:mb-4 "
                                style={{ fontSize: 'clamp(1.25rem, 4vw, 2rem)' }} /* Proportional title */
                            >
                                {content.title}
                            </h2>
                            <p
                                className="font-['Inter'] text-center leading-relaxed"
                                style={{ fontSize: 'clamp(0.875rem, 2.5vw, 1.125rem)' }} /* Proportional text */
                            >
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
