import React, { useEffect } from "react";
import { motion } from "framer-motion";
import { PiArrowBendDownRightThin } from "react-icons/pi";
import { CgCalendarDates } from "react-icons/cg";
import { FaTruck, FaStar, FaUserFriends, FaClock, FaGlobe, FaRobot, FaStopwatch, FaAd, FaVideo, FaBlog, FaChartLine, FaCalendarAlt, FaHeadset, FaRegCalendarCheck, FaPhoneVolume, FaEnvelopeOpenText } from "react-icons/fa";
import { SlEnergy } from "react-icons/sl";
import { RiBox3Fill, RiRobot2Line } from "react-icons/ri";
import { BsStars } from "react-icons/bs";
import { BiSolidReport } from "react-icons/bi";
import Modal from 'react-modal';
import { FaBangladeshiTakaSign } from "react-icons/fa6";
import { MdCancel, MdEmail, MdMail, MdOutlineCancel, MdSms } from "react-icons/md";
import { Link } from "react-router-dom";
import ContactForm from "../ContactForm/ContactForm";
import TopModal from "../TopModal/TopModal";

export const priceData = [
  {
    smBtn: "starter",
    title: "Best for solopreneurs or startups wanting fast automation.",
    price: "$499",
    priceInfo: "Check price in EU €",
    demoBtn: "Book a demo",
    serviceTitle: "What is included:",
    services: [
      { icon: <FaTruck />, label: "Smart Logo + Branding" },
      { icon: <FaStar />, label: "1-Page Website" },
      { icon: <SlEnergy />, label: "Instagram Setup + 5 Captions via AI" },
      { icon: <FaUserFriends />, label: " 1 AI Video Ad" },
      { icon: <FaRobot />, label: " AI Chatbot (Website Only)" },
      { icon: <FaGlobe />, label: " Free Online Brand Audit" },
      { icon: <FaClock />, label: "7 Days Delivery" },
    ],
  },
  {
    smBtn: "AI Growth Engine",
    title: "Ideal for local businesses scaling lead gen & automation.",
    price: " $999",
    priceInfo: "Check price in EU €",
    demoBtn: "Book a demo",
    serviceTitle: "What is included:",
    services: [
      { icon: <FaBangladeshiTakaSign />, label: " All from Starter Package" },
      { icon: <RiBox3Fill />, label: "WhatsApp Chatbot + FAQ Assistant" },
      { icon: <SlEnergy />, label: "5-Page SEO Website" },
      { icon: <FaUserFriends />, label: "AI Blog (1/Month)" },
      { icon: <FaStopwatch />, label: "CRM + AI-Powered Follow-up Reminders" },
      { icon: <FaGlobe />, label: " Social Media Content (10 AI-Crafted Posts + Captions)" },
      { icon: <MdMail />, label: "Email Marketing Setup (1 AI campaign/month)" },
      { icon: <FaClock />, label: "2 Weeks Delivery" },
    ],
  },
  {
    smBtn: "AI Dominator Suite",
    title: "High-impact funnel + full automation + ad management.",
    price: "$1,799",
    priceInfo: "Check price in EU €",
    demoBtn: "Book a demo",
    serviceTitle: "What is included:",
    services: [
      {
        icon: <BsStars className="text-primary" />,
        label: "Everything in Growth Engine"
      },
      {
        icon: <BiSolidReport className="text-primary" />,
        label: "Full Funnel Page (Conversion Optimized)"
      },
      {
        icon: <FaAd className="text-primary" />,
        label: "Meta & Google Ad Setup with AI Ad Copy & Split Tests"
      },
      {
        icon: <FaVideo className="text-primary" />,
        label: "2 AI Video Ads / Reels"
      },
      {
        icon: <FaBlog className="text-primary" />,
        label: "2 Blog Posts + SEO Optimization"
      },
      {
        icon: <FaChartLine className="text-primary" />,
        label: "AI Weekly Report with Actionable Insights"
      },
      {
        icon: <RiRobot2Line className="text-primary" />,
        label: "Custom GPT Assistant for Lead Qualification"
      },
      {
        icon: <MdEmail className="text-primary" />,
        label: "30-Day Email Automation"
      },
      {
        icon: <MdSms className="text-primary" />,
        label: "30-Day SMS Automation"
      },
      {
        icon: <FaCalendarAlt className="text-primary" />,
        label: "1-on-1 Strategy Call Monthly"
      },
      {
        icon: <FaHeadset className="text-primary" />,
        label: "3 Weeks Delivery + 30 Days Support"
      }
    ]
  },
  {
    smBtn: "AI-Powered Monthly Retainer",
    title: "(Post-setup ongoing growth)",
    price: "$699/month",
    priceInfo: "Check price in EU €",
    demoBtn: "Book a demo",
    serviceTitle: "What is included:",
    services: [
      {
        icon: <FaRegCalendarCheck className="text-primary" />,
        label: "Weekly AI Posts & Reels"
      },
      {
        icon: <FaAd className="text-primary" />,
        label: "Ads Management (Google + Meta)"
      },
      {
        icon: <FaBlog className="text-primary" />,
        label: "Monthly Blog + AI Report"
      },
      {
        icon: <FaEnvelopeOpenText className="text-primary" />,
        label: "Email Campaigns (2/Month)"
      },
      {
        icon: <RiRobot2Line className="text-primary" />,
        label: "Chatbot Tuning & CRM Optimization"
      },
      {
        icon: <FaPhoneVolume className="text-primary" />,
        label: "Monthly Consulting Call"
      }
    ]
  }
];

const Plans = () => {
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
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        type: "spring",
        stiffness: 100,
        damping: 10
      }
    }
  };

  const [isModalOpen, setIsModalOpen] = React.useState(false);

  return (
    <div className="bg-six py-5 pb-20">
      {/* Title */}
      <motion.h1
        className="text-4xl md:text-7xl font-semibold text-center text-white glowing-green mb-12"
        initial={{ opacity: 0, y: -20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
      >
        Our Plans
      </motion.h1>

      {/* Content Grid */}
      <div className="flex flex-col gap-8 max-w-7xl mx-auto px-4">
        {/* Left Column - Header */}
        <div className=" pt-16 flex flex-col items-center px-4 text-white text-center md:px-20">
          <motion.h1
            className="text-2xl md:text-5xl font-bold mb-6"
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <span className="text-primary">Grow your business</span> with our
            CX tools and affordable fulfilment
          </motion.h1>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <button onClick={() => setIsModalOpen(!isModalOpen)} className="flex items-center gap-2 bg-primary hover:bg-white hover:text-primary text-white px-4 py-2 rounded-lg transition-colors duration-300 mb-6">
              <CgCalendarDates className="text-xl" />
              Calculate your fulfilment prices
            </button>
          </motion.div>
          {
            <TopModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
              <ContactForm />
            </TopModal>



          }
          <motion.div
            className="flex items-start gap-2"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <PiArrowBendDownRightThin className="text-3xl glowing-green" />
            <p>BtoC and BtoB logistics to scale your brand</p>
          </motion.div>
        </div>

        {/* Right Column - Cards */}
        <motion.div
          className=""
          initial="hidden"
          whileInView="visible"
          viewport={{ margin: "-100px" }}
          variants={container}
        >
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 md:gap-2 pb-6 px-4">
            {priceData.map((e, i) => (
              <motion.div
                key={i}
                className={`flex-none w-full ${i === 1 ? "lg:-translate-y-6 max-lg:mb-10" : ""} glow-hover transition-all duration-500 rounded-3xl`}
                variants={item}
              >
                <div className={`rounded-3xl ${i === 1 ? "bg-primary " : ""} h-full`}>
                  {i === 1 && (
                    <p className="text-white text-center py-2 glowing-green">
                      Most Popular
                    </p>
                  )}
                  <div className={`bg-white p-6 rounded-3xl flex flex-col gap-4 h-full ${i === 1 ? "border-2 border-primary " : ""}`}>
                    <div className="flex flex-col items-center gap-3">
                      <button className={`px-5 py-1 rounded-full border-primary border text-primary`}>
                        {e.smBtn}
                      </button>
                      <p className="text-center text-gray-600">{e.title}</p>
                      <h1 className="text-3xl font-bold text-gray-900">{e.price}</h1>
                      {/* <p className="text-sm text-gray-500">{e.priceInfo}</p> */}
                    </div>
                    <Link to={"/Contact"}
                      className={`w-full py-3 text-center rounded-lg ${i === 1 ? "bg-primary text-white glow-hover" : "border border-primary text-primary hover:bg-primary hover:text-white"} transition-colors duration-300`}
                    >
                      {e.demoBtn}
                    </Link>

                    <div className="flex flex-col gap-2">
                      <h4 className="text-sm text-gray-500">{e.serviceTitle}</h4>
                      {e.services.map((val, index) => (
                        <div key={index} className="flex items-center gap-2 text-sm">
                          <span className="text-primary">{val.icon}</span>
                          <p>{val.label}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Plans;