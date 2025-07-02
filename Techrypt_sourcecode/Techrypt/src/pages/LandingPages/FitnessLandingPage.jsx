import React from 'react';
import styles from './FitnessLandingPage.module.css';
import { motion } from 'framer-motion';
import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/effect-coverflow';
import { EffectCoverflow, Autoplay } from 'swiper/modules';
import { useNavigate } from 'react-router-dom';
import { Zap, Palette, Laptop, TrendingUp, Bot, BarChart, Ban, LineChart,  Monitor, Moon } from 'lucide-react';

import TechryptChatbot from "../../components/TechryptChatbot/TechryptChatbot";

// Hero Section
const HeroSection = ({ onOpenAppointment }) => (
  <section className={styles.heroSection}>
    <motion.h1
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7 }}
      className={styles.heroTitle}
    >
      Fuel Your <span className={styles.neonGreen}>Fitness Brand’s Growth</span>
    </motion.h1>
    <motion.p
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2, duration: 0.7 }}
      className={styles.heroSubtitle}
    >
      We help gyms, trainers, and wellness brands dominate online with bold digital strategy, design, and automation.
    </motion.p>
    <motion.button
      whileHover={{ scale: 1.08, backgroundColor: '#c4d322', color: '#181818' }}
      className={styles.ctaBtn}
      onClick={onOpenAppointment}
    >
      Build My Brand
    </motion.button>
    <div className={styles.heroBgOverlay}></div>
  </section>
);

// Problem Section
const problems = [
  { icon: <Ban size={32} stroke="url(#techrypt-gradient)" />, title: 'No Digital Presence' },
  { icon: <LineChart size={32} stroke="url(#techrypt-gradient)" />, title: 'Low Conversions' },
  { icon: <Moon size={32} stroke="url(#techrypt-gradient)" />, title: 'Weak Branding' }, // changed from Sleep to Moon
  { icon: <Monitor size={32} stroke="url(#techrypt-gradient)" />, title: 'Generic Websites' },
];
const ProblemSection = () => (
  <section className={styles.problemSection}>
    <motion.h2
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6 }}
      className={styles.sectionTitle}
    >
      Common Fitness Business Challenges
    </motion.h2>
    <div className={styles.problemGrid}>
      {problems.map((p, i) => (
        <motion.div
          key={p.title}
          className={styles.problemCard}
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: i * 0.1, duration: 0.5 }}
        >
          <span className={styles.problemIcon}>{p.icon}</span>
          <span className={styles.problemText}>{p.title}</span>
        </motion.div>
      ))}
    </div>
  </section>
);

// Solutions Section
const solutions = [
  { icon: <Zap size={36} stroke="url(#techrypt-gradient)" />, text: 'Brand Strategy & Positioning' },
  { icon: <Palette size={36} stroke="url(#techrypt-gradient)" />, text: 'Bold Fitness Design' },
  { icon: <Laptop size={36} stroke="url(#techrypt-gradient)" />, text: 'Custom Website & App Dev' },
  { icon: <TrendingUp size={36} stroke="url(#techrypt-gradient)" />, text: 'Paid Ads & SEO' },
  { icon: <Bot size={36} stroke="url(#techrypt-gradient)" />, text: 'AI Automation' },
{ icon: <LineChart size={36} stroke="url(#techrypt-gradient)" />, text: 'Analytics & Conversion' },
];
const SolutionsSection = () => (
  <section className={styles.solutionsSection}>
    <motion.h2
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6 }}
      className={styles.sectionTitle}
    >
      How We Power Up Your Fitness Brand
    </motion.h2>
    <div className={styles.solutionsGrid}>
      {solutions.map((s, i) => (
        <motion.div
          key={s.text || `icon-only-${i}`}
          className={styles.solutionCard}
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ delay: i * 0.08, duration: 0.4 }}
        >
          <span className={styles.solutionIcon}>{s.icon}</span>
          {s.text && <span className={styles.solutionText}>{s.text}</span>}
        </motion.div>
      ))}
    </div>
  </section>
);

// Services Section
const allServices = [
  { label: 'Branding & Logo Design' },
  { label: 'Website (WordPress/Shopify)' },
  { label: 'SEO' },
  { label: 'Paid Ads' },
  { label: 'UI/UX' },
  { label: 'Enterprise Cyber Solutions' },
  { label: 'AI-Based Marketing' },
  { label: 'SaaS Dev for Fitness Platforms' },
  { label: 'Custom Web Apps' },
  { label: 'Mobile Apps' },
  { label: 'Cybersecurity for Fitness' },
  { label: 'AI Chatbots' },
];
const ServicesSection = () => {
  const navigate = useNavigate();
  const swiperRef = React.useRef(null);

  // Pause autoplay on mouse enter, resume on mouse leave
  const handleMouseEnter = () => {
    if (swiperRef.current && swiperRef.current.autoplay) {
      swiperRef.current.autoplay.stop();
    }
  };
  const handleMouseLeave = () => {
    if (swiperRef.current && swiperRef.current.autoplay) {
      swiperRef.current.autoplay.start();
    }
  };

  return (
    <section className={styles.servicesSection} style={{ background: "#181818" }}>
      <h2 className={styles.sectionTitle}>Our Services</h2>
      <Swiper
        effect={'coverflow'}
        grabCursor={true}
        centeredSlides={true}
        slidesPerView={'auto'}
        loop={true}
        autoplay={{ delay: 1800, disableOnInteraction: false }}
        coverflowEffect={{
          rotate: 0,
          stretch: 60,
          depth: 120,
          modifier: 2.5,
          slideShadows: false,
        }}
        modules={[EffectCoverflow, Autoplay]}
        className={styles.servicesSwiper}
        style={{ padding: "2rem 0" }}
        onSwiper={swiper => { swiperRef.current = swiper; }}
      >
        {allServices.map((service, idx) => (
          <SwiperSlide
            key={service.label}
            className={styles.serviceSlide}
            onClick={() => navigate('/Services')}
            tabIndex={0}
            role="button"
            aria-label={`Go to Services for ${service.label}`}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
            onFocus={handleMouseEnter}
            onBlur={handleMouseLeave}
          >
            <span className={styles.serviceSlideText}>{service.label}</span>
          </SwiperSlide>
        ))}
      </Swiper>
    </section>
  );
};

// CTA Blocks
const CTASection = ({ onOpenAppointment }) => (
  <section className={styles.ctaSection}>
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
      className={styles.ctaBlock}
    >
      <h2 className={styles.ctaTitle}>Book a Free Strategy Call</h2>
      <button className={styles.ctaBtnAlt} onClick={onOpenAppointment}>Book Now</button>
    </motion.div>
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true }}
      transition={{ delay: 0.2, duration: 0.5 }}
      className={styles.ctaBlock}
    >
      <h2 className={styles.ctaTitle}>Launch My Fitness App Today</h2>
      <button className={styles.ctaBtnAlt} onClick={onOpenAppointment}>Get Started</button>
    </motion.div>
  </section>
);

const IconGradientDefs = () => (
  <svg width="0" height="0">
    <defs>
      <linearGradient id="techrypt-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop stopColor="#c4d322" offset="0%" />
        <stop stopColor="#8c9719" offset="100%" />
      </linearGradient>
    </defs>
  </svg>
);

const FitnessLandingPage = () => {
  const [showAppointment, setShowAppointment] = React.useState(false);
  const [openAppointmentDirect, setOpenAppointmentDirect] = React.useState(false);

  const handleOpenAppointment = () => {
    setOpenAppointmentDirect(true);
    setShowAppointment(true);
  };

  return (
    <div className={styles.fitnessLandingRoot}>
      <HeroSection onOpenAppointment={handleOpenAppointment} />
      <ProblemSection />
      <SolutionsSection />
      <ServicesSection />
      <CTASection onOpenAppointment={handleOpenAppointment} />
      {showAppointment && (
        <TechryptChatbot
          isOpen={showAppointment}
          onClose={() => {
            setShowAppointment(false);
            setOpenAppointmentDirect(false);
          }}
          openAppointmentDirect={openAppointmentDirect}
        />
      )}
      <IconGradientDefs />
    </div>
  );
};

export default FitnessLandingPage;