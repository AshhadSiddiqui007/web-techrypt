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
    smBtn: "Free Trial",
    title: "Test the core bot before committing.",
    price: "7 Days Free",
    priceInfo: "No credit card required",
    demoBtn: "Try It Free for 7 Days",
    serviceTitle: "What's included:",
    services: [
      { icon: <FaRobot />, label: "AI chatbot installed on your site (1 page)" },
      { icon: <FaStar />, label: "Basic reply logic (up to 5 questions)" },
      { icon: <FaGlobe />, label: "Lead capture sent to Google Sheet" },
      { icon: <FaCalendarAlt />, label: "Appointment booking (Calendly/TidyCal)" },
      { icon: <MdMail />, label: "1 follow-up message flow" },
      { icon: <FaTruck />, label: "Bot branded with Techrypt watermark" },
      { icon: <FaHeadset />, label: "Email support during trial" },
    ],
  },
  {
    smBtn: "Growth Package",
    title: "Best for service businesses wanting full automation with simple workflows.",
    price: "$499 Setup",
    priceInfo: "$49 per month",
    demoBtn: "Upgrade to Growth",
    serviceTitle: "What's included:",
    services: [
      { icon: <FaRobot />, label: "Full AI chatbot (up to 10 logic flows)" },
      { icon: <FaStar />, label: "Branded with your business identity" },
      { icon: <RiBox3Fill />, label: "CRM integration" },
      { icon: <FaCalendarAlt />, label: "Booking integration with custom confirmation flow" },
      { icon: <FaChartLine />, label: "Monthly basic performance report" },
      { icon: <FaHeadset />, label: "Priority email support" },
      { icon: <FaGlobe />, label: "Watermark removed" },
    ],
  },
  {
    smBtn: "Pro Scale Package",
    title: "For serious businesses ready to scale with funnels, ads, and real-time data.",
    price: "Custom Prices",
    priceInfo: "Contact for pricing",
    demoBtn: "Contact for Pro Scale",
    serviceTitle: "What's included:",
    services: [
      {
        icon: <BsStars className="text-primary" />,
        label: "Everything in Growth Package"
      },
      {
        icon: <BiSolidReport className="text-primary" />,
        label: "1–2 page custom funnel (Landing + Thank You)"
      },
      {
        icon: <FaAd className="text-primary" />,
        label: "Meta Ads integration (Facebook + Instagram)"
      },
      {
        icon: <FaChartLine className="text-primary" />,
        label: "Real-time analytics dashboard"
      },
      {
        icon: <FaPhoneVolume className="text-primary" />,
        label: "Monthly strategy call & conversion audit"
      },
      {
        icon: <FaHeadset className="text-primary" />,
        label: "Priority support via WhatsApp/email"
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
            <span className="text-primary">Scale your business</span> with AI
            chatbots and automation tools
          </motion.h1>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
        
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
            <p>From basic bots to advanced funnels with real-time analytics</p>
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
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12 md:gap-2 pb-6 px-4">
            {priceData.map((e, i) => (
              <motion.div
                key={i}
                className={`flex-none w-full ${i === 1 ? "lg:-translate-y-6 max-lg:mb-12" : ""} ${i === 2 ? "max-lg:mt-12" : ""} glow-hover transition-all duration-500 rounded-3xl`}
                variants={item}
              >
                <div className={`rounded-3xl ${i === 1 ? "bg-primary " : ""} ${i === 2 ? "max-lg:pt-16" : ""} h-full`}>
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