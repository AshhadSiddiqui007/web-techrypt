import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  TrendingDown, 
  Users, 
  Calendar, 
  DollarSign,
  Smartphone,
  Globe,
  Bot,
  BarChart3,
  Zap,
  Target,
  MessageSquare,
  Award
} from 'lucide-react';

import TechryptChatbot from "../../components/TechryptChatbot/TechryptChatbot";
import FitnessChatUI from "../../components/FitnessLandingPage/FitnessChatUI";

// Hero Section
const HeroSection = ({ onOpenAppointment }) => (
  <section className="min-h-screen bg-gradient-to-br from-[#181818] via-[#1a1a1a] to-[#0f0f0f] flex items-center justify-center relative overflow-hidden">
    {/* Animated Background Elements */}
    <div className="absolute inset-0">
      <motion.div 
        className="absolute top-20 left-10 w-72 h-72 bg-[#C4D322]/10 rounded-full blur-3xl"
        animate={{
          x: [0, 50, -30, 0],
          y: [0, -30, 20, 0],
          scale: [1, 1.2, 0.8, 1],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          repeatType: "reverse"
        }}
      ></motion.div>
      <motion.div 
        className="absolute bottom-20 right-10 w-96 h-96 bg-[#C4D322]/5 rounded-full blur-3xl"
        animate={{
          x: [0, -40, 60, 0],
          y: [0, 40, -20, 0],
          scale: [1, 0.7, 1.3, 1],
        }}
        transition={{
          duration: 10,
          repeat: Infinity,
          repeatType: "reverse"
        }}
      ></motion.div>
    </div>
    
    <div className="container mx-auto px-6 relative z-10">
      <div className="grid lg:grid-cols-2 gap-12 items-center">
        {/* Left Column - Content */}
        <div className="text-center lg:text-left">
          <motion.h1
            initial={{ opacity: 0, y: 40, rotateX: -15 }}
            animate={{ opacity: 1, y: 0, rotateX: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="text-4xl md:text-6xl lg:text-7xl font-bold text-white mb-6"
          >
            <motion.span
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3, duration: 0.6, type: "spring", stiffness: 100 }}
            >
              Transform Your{' '}
            </motion.span>
            <motion.span 
              className="text-transparent bg-clip-text bg-gradient-to-r from-[#C4D322] to-[#A8B91A]"
              initial={{ opacity: 0, scale: 0.5, rotateY: 45 }}
              animate={{ opacity: 1, scale: 1, rotateY: 0 }}
              transition={{ delay: 0.6, duration: 0.8, type: "spring", stiffness: 80 }}
            >
              Fitness Business
            </motion.span>
          </motion.h1>
          
          <motion.p
            initial={{ opacity: 0, y: 30, blur: 10 }}
            animate={{ opacity: 1, y: 0, blur: 0 }}
            transition={{ delay: 0.9, duration: 0.8, ease: "easeOut" }}
            className="text-lg md:text-xl lg:text-2xl text-gray-300 mb-8 max-w-2xl lg:mx-0 mx-auto leading-relaxed"
          >
            Stop losing members to competitors. Get the digital tools and automation that turn your gym into a client magnet.
          </motion.p>
          
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.8 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ delay: 1.2, duration: 0.8, type: "spring", stiffness: 100 }}
            className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start items-center"
          >
            <motion.button
              onClick={onOpenAppointment}
              className="px-6 md:px-8 py-3 md:py-4 bg-gradient-to-r from-[#C4D322] to-[#A8B91A] text-[#181818] font-bold text-base md:text-lg rounded-lg hover:shadow-2xl hover:shadow-[#C4D322]/20 transition-all duration-300 transform hover:scale-105"
              whileHover={{ 
                scale: 1.05, 
                rotate: [0, -1, 1, 0],
                boxShadow: "0 25px 50px -12px rgba(196, 211, 34, 0.3)"
              }}
              whileTap={{ scale: 0.95, rotate: 0 }}
              animate={{
                y: [0, -5, 0],
              }}
              transition={{
                y: {
                  duration: 2,
                  repeat: Infinity,
                  repeatType: "reverse",
                  ease: "easeInOut"
                }
              }}
            >
              Get Your Free Fitness Marketing Audit
            </motion.button>
            <motion.span 
              className="text-gray-400 text-sm md:text-base"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 1.5, duration: 0.6 }}
            >
              No commitment • 15-minute call
            </motion.span>
          </motion.div>
        </div>

        {/* Right Column - Fitness Chat UI */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8, rotateY: 45 }}
          animate={{ opacity: 1, scale: 1, rotateY: 0 }}
          transition={{ delay: 0.5, duration: 1, type: "spring", stiffness: 80 }}
          className="flex justify-center lg:justify-end"
        >
          <FitnessChatUI />
        </motion.div>
      </div>
    </div>
  </section>
);

// Pain Points Section
const painPoints = [
  {
    icon: <TrendingDown className="w-12 h-12 text-[#C4D322]" />,
    title: "Declining Memberships",
    description: "Members are canceling faster than you can sign them up, and you're not sure why."
  },
  {
    icon: <Users className="w-12 h-12 text-[#C4D322]" />,
    title: "Low Online Visibility", 
    description: "Your gym doesn't show up when people search for fitness in your area."
  },
  {
    icon: <Calendar className="w-12 h-12 text-[#C4D322]" />,
    title: "Manual Booking Chaos",
    description: "Staff spend hours on phone calls and emails just to schedule classes and sessions."
  },
  {
    icon: <DollarSign className="w-12 h-12 text-[#C4D322]" />,
    title: "Revenue Plateaus",
    description: "You're stuck at the same revenue level while costs keep rising."
  }
];

const PainPointsSection = () => (
  <section className="py-20 bg-[#0f0f0f]">
    <div className="container mx-auto px-6">
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-16"
      >
        <motion.h2 
          className="text-4xl md:text-5xl font-bold text-white mb-6"
          initial={{ opacity: 0, scale: 0.5 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, type: "spring", stiffness: 100 }}
        >
          Sound Familiar? You're Not Alone.
        </motion.h2>
        <motion.p 
          className="text-xl text-gray-300 max-w-3xl mx-auto"
          initial={{ opacity: 0, x: -50 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.3, duration: 0.6 }}
        >
          95% of fitness businesses struggle with these exact same challenges. Here's what's really happening:
        </motion.p>
      </motion.div>
      
      <div className="grid lg:grid-cols-2 gap-12 items-center">
        {/* Left Column - Fitness Animation */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8, rotateY: 45 }}
          whileInView={{ opacity: 1, scale: 1, rotateY: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.5, duration: 1, type: "spring", stiffness: 80 }}
          className="flex justify-center"
        >
          <div className="fitness-animation-container">
            <style jsx>{`
              .fitness-animation-container {
                position: relative;
                margin: 20px auto;
                border-radius: 20px;
                background: #C4D322;
                width: 400px;
                height: 300px;
                overflow: hidden;
              }
              
              @media (max-width: 768px) {
                .fitness-animation-container {
                  width: 300px;
                  height: 225px;
                  transform: scale(0.8);
                }
              }

              .man {
                position: absolute;
                top: 40%;
                left: 25%;
                width: 55%;
                height: 45%;
                z-index: 3;
              }

              .man .legs {
                position: absolute;
                width: 20%;
                height: 64%;
                bottom: 4%;
              }

              .man .legs .leg {
                position: absolute;
                width: 20%;
                height: 100%;
                border-top-left-radius: 30px;
                border-top-right-radius: 30px;
              }

              .man .legs .leg::after {
                content: "";
                background: #000;
                position: absolute;
                width: 100%;
                height: 5%;
                bottom: 0;
              }

              .man .legs .leg::before {
                content: "";
                background: #000;
                position: absolute;
                width: 50%;
                height: 5%;
                bottom: 3px;
                left: -12%;
                border-radius: 50%;
              }

              .man .legs .one {
                background: #ffffff;
                left: 20%;
                z-index: 3;
              }

              .man .legs .two {
                background: #f0f0f0;
                left: 10%;
                z-index: 2;
                transform: rotate(10deg);
              }

              .man .legs .thy {
                z-index: 2;
                position: absolute;
                height: 12%;
                width: 120%;
                left: 24%;
                background: #181818;
              }

              .man .legs .thy::after {
                content: "";
                position: absolute;
                border-top-left-radius: 40%;
                border-bottom-left-radius: 40%;
                top: -70%;
                height: 240%;
                width: 25%;
                right: -20%;
                background-color: #181818;
              }

              .man .main-parts {
                position: absolute;
                left: 33%;
                width: 40%;
                height: 30%;
                top: 15%;
              }

              .man .main-parts .upper {
                position: absolute;
                height: 30%;
                width: 48%;
                bottom: 36%;
                background: #C4D322;
                z-index: 1;
                transform: rotate(-5deg);
              }

              .man .main-parts .upper .above {
                position: absolute;
                right: 0;
                background: #C4D322;
                width: 150%;
                height: 331%;
                border-radius: 50%;
                right: -104%;
                top: -92%;
              }

              .man .main-parts .lower {
                position: absolute;
                height: 40%;
                width: 100%;
                bottom: 0%;
                background: #A8B91A;
                z-index: 2;
              }

              .man .main-parts .lower::after {
                content: "";
                position: absolute;
                height: 201%;
                width: 56%;
                right: 0;
                top: -99%;
                border-radius: 100%;
                background: #A8B91A;
              }

              .man .hand {
                position: absolute;
                right: 28%;
                height: 40%;
                width: 9%;
                border-radius: 20px;
                background: #ffffff;
                z-index: 5;
                top: 12%;
                animation: animate-hand 2s infinite;
              }

              .man .weight {
                position: absolute;
                height: 30%;
                width: 18%;
                border-radius: 50%;
                border: 4px solid #000;
                left: 57%;
                top: -10%;
                background: #C4D322;
                z-index: 10;
                animation: animate-hand 2s infinite;
              }

              .man .weight:after {
                content: "";
                background-color: #A8B91A;
                position: absolute;
                width: 60%;
                height: 60%;
                border-radius: 50%;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
              }

              .man .weight:before {
                content: "";
                background-color: #181818;
                position: absolute;
                width: 20%;
                height: 20%;
                border-radius: 50%;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 1;
              }

              @keyframes animate-hand {
                50% {
                  transform: translateY(-40px);
                }
              }

              .man .arm {
                position: absolute;
                right: 28%;
                width: 10%;
                height: 10%;
                z-index: 5;
                top: 88px;
                background: #f0f0f0;
                border-radius: 30px 5px 5px 30px;
              }

              .man .neck {
                position: absolute;
                left: 73%;
                width: 20%;
                height: 12%;
                background: #f0f0f0;
                top: 32%;
                overflow: hidden;
              }

              .man .neck .head {
                position: absolute;
                right: 0;
                bottom: -8%;
                width: 69%;
                height: 166%;
                border-radius: 50%;
                background: #ffffff;
              }

              .man .nose {
                width: 10%;
                height: 10%;
                position: absolute;
                right: 5%;
                top: 21%;
                display: flex;
                justify-content: space-evenly;
              }

              .man .nose div {
                position: absolute;
                bottom: -24%;
                width: 7px;
                height: 10px;
                border-radius: 50%;
                background: #ffffff;
              }

              .man .nose div:nth-child(1) {
                left: 10%;
              }

              .man .nose div:nth-child(2) {
                left: 50%;
              }

              .man .hairs {
                position: absolute;
                left: 86%;
                height: 20%;
                width: 10%;
                top: 23%;
              }

              .man .hairs .lower {
                position: absolute;
                bottom: -3px;
                right: 11px;
                width: 70%;
                height: 33%;
                background: #000;
                border-radius: 4px;
                border-bottom-right-radius: 20%;
              }

              .man .hairs .lower::after {
                content: "";
                position: absolute;
                width: 24%;
                height: 40%;
                border-radius: 50%;
                background: #ffffff;
              }

              .man .hairs .upper {
                position: absolute;
                right: -10%;
                bottom: 0;
                height: 80%;
                width: 40%;
              }

              .man .hairs .upper div:nth-child(1) {
                position: absolute;
                width: 100%;
                height: 40%;
                background: #000;
                border-radius: 50%;
              }

              .man .hairs .upper div:nth-child(2) {
                position: absolute;
                top: 30%;
                width: 100%;
                height: 40%;
                background: #000;
                border-radius: 50%;
              }

              .man .hairs .upper div:nth-child(3) {
                position: absolute;
                top: 60%;
                width: 100%;
                height: 40%;
                background: #000;
                border-radius: 50%;
              }

              .bench-container {
                position: absolute;
                top: 60%;
                left: 40%;
                width: 45%;
                height: 25%;
                z-index: 2;
              }

              .bench-container .left {
                position: absolute;
                top: 10%;
                left: 0;
                background: #181818;
                width: 5%;
                height: 90%;
              }

              .bench-container .left::after {
                content: "";
                position: absolute;
                width: 300%;
                height: 10%;
                left: -100%;
                bottom: 0;
                border-top: 4px solid #000;
                background: #181818;
              }

              .bench-container .right {
                z-index: -1;
                position: absolute;
                top: -100%;
                right: 5%;
                background: #181818;
                width: 5%;
                height: 200%;
              }

              .bench-container .right::after {
                content: "";
                position: absolute;
                width: 400%;
                height: 5%;
                left: -150%;
                bottom: 0;
                border-top: 4px solid #000;
                background: #181818;
              }

              .seat {
                position: absolute;
                width: 100%;
                background: #ffffff;
                height: 10%;
                border-radius: 15px 15px 0 0;
              }

              .rod1 {
                position: absolute;
                top: 70%;
                height: 15%;
                width: 40%;
                right: 5%;
                z-index: 1;
              }
            `}</style>
            
            <div className="bench-container">
              <div className="seat"></div>
              <div className="left"></div>
              <div className="right"></div>
            </div>
            <div className="man">
              <div className="legs">
                <div className="leg one"></div>
                <div className="leg two"></div>
                <div className="thy"></div>
              </div>
              <div className="main-parts">
                <div className="lower"></div>
                <div className="upper">
                  <div className="above"></div>
                </div>
              </div>
              <div className="neck">
                <div className="head"></div>
              </div>
              <div className="arm"></div>
              <div className="nose">
                <div></div>
                <div></div>
              </div>
              <div className="hairs">
                <div className="lower"></div>
                <div className="upper">
                  <div></div>
                  <div></div>
                  <div></div>
                </div>
              </div>
              <div className="hand"></div>
              <div className="weight"></div>
            </div>
            <div className="rod1"></div>
          </div>
        </motion.div>

        {/* Right Column - Pain Points stacked vertically */}
        <div className="space-y-6">
          {painPoints.map((point, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: 100, rotateY: 45 }}
              whileInView={{ opacity: 1, x: 0, rotateY: 0 }}
              viewport={{ once: true }}
              transition={{ 
                delay: index * 0.15,
                duration: 0.8,
                type: "spring",
                stiffness: 100
              }}
              whileHover={{ 
                x: 10,
                scale: 1.02,
                transition: { duration: 0.3 }
              }}
              className="bg-gradient-to-br from-[#1a1a1a] to-[#181818] p-6 rounded-2xl border border-[#C4D322]/20 hover:border-[#C4D322]/40 transition-all duration-300 group"
            >
              <div className="flex items-start gap-4">
                <motion.div 
                  className="flex-shrink-0"
                  initial={{ scale: 0, rotate: -180 }}
                  whileInView={{ scale: 1, rotate: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.15 + 0.3, duration: 0.6, type: "spring" }}
                  whileHover={{ 
                    rotate: [0, -10, 10, 0],
                    scale: 1.1
                  }}
                >
                  {point.icon}
                </motion.div>
                <div>
                  <motion.h3 
                    className="text-xl font-bold text-white mb-2"
                    initial={{ opacity: 0, y: 10 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.15 + 0.5, duration: 0.5 }}
                  >
                    {point.title}
                  </motion.h3>
                  <motion.p 
                    className="text-gray-400"
                    initial={{ opacity: 0, y: 10 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.15 + 0.7, duration: 0.5 }}
                  >
                    {point.description}
                  </motion.p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  </section>
);

// Soft Solutions Section
const softSolutions = [
  {
    icon: <Globe className="w-8 h-8 text-[#C4D322]" />,
    title: "Professional Website & SEO",
    description: "Get found when people search for gyms in your area"
  },
  {
    icon: <Bot className="w-8 h-8 text-[#C4D322]" />,
    title: "AI-Powered Lead Capture",
    description: "Never miss a potential member inquiry again"
  },
  {
    icon: <Smartphone className="w-8 h-8 text-[#C4D322]" />,
    title: "Mobile App Development",
    description: "Keep members engaged with your own branded fitness app"
  },
  {
    icon: <BarChart3 className="w-8 h-8 text-[#C4D322]" />,
    title: "Data Analytics & Insights",
    description: "Know exactly what's working and what isn't"
  },
  {
    icon: <MessageSquare className="w-8 h-8 text-[#C4D322]" />,
    title: "Social Media Automation",
    description: "Stay active on social without the daily hassle"
  },
  {
    icon: <Target className="w-8 h-8 text-[#C4D322]" />,
    title: "Targeted Ad Campaigns",
    description: "Reach the right people at the right time with precision"
  }
];

const SoftSolutionsSection = () => (
  <section className="py-20 bg-[#181818]">
    <div className="container mx-auto px-6">
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-16"
      >
        <motion.h2 
          className="text-4xl md:text-5xl font-bold text-white mb-6"
          initial={{ opacity: 0, rotateX: 90 }}
          whileInView={{ opacity: 1, rotateX: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          What If There Was a{' '}
          <motion.span 
            className="text-transparent bg-clip-text bg-gradient-to-r from-[#C4D322] to-[#A8B91A]"
            initial={{ opacity: 0, scale: 0.3, skewX: 45 }}
            whileInView={{ opacity: 1, scale: 1, skewX: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.3, duration: 0.8, type: "spring", stiffness: 80 }}
          >
            Better Way?
          </motion.span>
        </motion.h2>
        <motion.p 
          className="text-xl text-gray-300 max-w-3xl mx-auto"
          initial={{ opacity: 0, scale: 0.8 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.5, duration: 0.6 }}
        >
          Imagine if your fitness business had the same digital advantages as the big chain gyms...
        </motion.p>
      </motion.div>
      
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {softSolutions.map((solution, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: index % 2 === 0 ? -100 : 100, rotateY: index % 2 === 0 ? -45 : 45 }}
            whileInView={{ opacity: 1, x: 0, rotateY: 0 }}
            viewport={{ once: true }}
            transition={{ 
              delay: index * 0.1,
              duration: 0.8,
              type: "spring",
              stiffness: 60
            }}
            whileHover={{ 
              scale: 1.05,
              rotateX: 5,
              boxShadow: "0 20px 40px rgba(196, 211, 34, 0.1)",
              transition: { duration: 0.3 }
            }}
            className="bg-gradient-to-br from-[#1a1a1a] to-[#0f0f0f] p-6 rounded-xl border border-gray-800 hover:border-[#C4D322]/30 transition-all duration-300 group"
          >
            <div className="flex items-start gap-4">
              <motion.div 
                className="p-2 bg-[#C4D322]/10 rounded-lg group-hover:bg-[#C4D322]/20 transition-colors"
                whileHover={{ 
                  rotate: [0, -15, 15, 0],
                  scale: 1.1
                }}
                transition={{ duration: 0.5 }}
              >
                {solution.icon}
              </motion.div>
              <div>
                <motion.h3 
                  className="text-lg font-semibold text-white mb-2"
                  initial={{ opacity: 0, y: 10 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 + 0.3, duration: 0.5 }}
                >
                  {solution.title}
                </motion.h3>
                <motion.p 
                  className="text-gray-400 text-sm"
                  initial={{ opacity: 0, y: 10 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 + 0.5, duration: 0.5 }}
                >
                  {solution.description}
                </motion.p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

// Hard Selling Services Section
const mainServices = [
  {
    icon: <Globe className="w-16 h-16 text-[#181818]" />,
    title: "Complete Digital Presence",
    description: "Professional website, SEO optimization, and local search dominance",
    features: ["Custom fitness website design", "Local SEO optimization", "Google Business optimization", "Mobile-responsive design"],
  },
  {
    icon: <Bot className="w-16 h-16 text-[#181818]" />,
    title: "AI Automation Suite",
    description: "24/7 lead capture, booking automation, and member communication",
    features: ["AI chatbot for inquiries", "Automated booking system", "Follow-up sequences", "Member retention campaigns"],
  },
  {
    icon: <Smartphone className="w-16 h-16 text-[#181818]" />,
    title: "Custom Fitness App",
    description: "Your own branded mobile app for member engagement and retention",
    features: ["Workout tracking", "Class scheduling", "Progress monitoring", "Push notifications"],
  }
];

const HardSellingSection = ({ onOpenAppointment }) => (
  <section className="py-20 bg-gradient-to-br from-[#0f0f0f] to-[#181818]">
    <div className="container mx-auto px-6">
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-16"
      >
        <motion.h2 
          className="text-4xl md:text-5xl font-bold text-white mb-6"
          initial={{ opacity: 0, y: 50, scale: 0.8 }}
          whileInView={{ opacity: 1, y: 0, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, type: "spring", stiffness: 100 }}
        >
          Here's How We Make It{' '}
          <motion.span 
            className="text-transparent bg-clip-text bg-gradient-to-r from-[#C4D322] to-[#A8B91A]"
            initial={{ opacity: 0, rotateY: 90, scale: 0.5 }}
            whileInView={{ opacity: 1, rotateY: 0, scale: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.3, duration: 0.8, type: "spring", stiffness: 80 }}
          >
            Happen
          </motion.span>
        </motion.h2>
        <motion.p 
          className="text-xl text-gray-300 max-w-3xl mx-auto"
          initial={{ opacity: 0, blur: 10 }}
          whileInView={{ opacity: 1, blur: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.5, duration: 0.6 }}
        >
          Three core services that will transform your fitness business in the next 90 days
        </motion.p>
      </motion.div>
      
      <div className="grid lg:grid-cols-3 gap-8">
        {mainServices.map((service, index) => (
          <motion.div
            key={index}
            initial={{ 
              opacity: 0, 
              y: 100, 
              rotateX: 45,
              scale: 0.8
            }}
            whileInView={{ 
              opacity: 1, 
              y: 0, 
              rotateX: 0,
              scale: 1
            }}
            viewport={{ once: true }}
            transition={{ 
              delay: index * 0.2,
              duration: 0.8,
              type: "spring",
              stiffness: 100
            }}
            whileHover={{ 
              y: -15,
              rotateY: 5,
              scale: 1.02,
              transition: { duration: 0.3 }
            }}
            className="bg-gradient-to-br from-[#1a1a1a] to-[#181818] p-8 rounded-2xl border border-[#C4D322]/30 hover:border-[#C4D322]/50 transition-all duration-300 relative overflow-hidden group"
          >
            {/* Animated Background effect */}
            <motion.div 
              className="absolute inset-0 bg-gradient-to-br from-[#C4D322]/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
              initial={{ scale: 0, rotate: 45 }}
              whileHover={{ scale: 1, rotate: 0 }}
              transition={{ duration: 0.5 }}
            ></motion.div>
            
            <div className="relative z-10">
              <motion.div 
                className="w-20 h-20 bg-gradient-to-br from-[#C4D322] to-[#A8B91A] rounded-2xl flex items-center justify-center mb-6 mx-auto"
                initial={{ scale: 0, rotate: -180 }}
                whileInView={{ scale: 1, rotate: 0 }}
                viewport={{ once: true }}
                transition={{ 
                  delay: index * 0.2 + 0.3,
                  duration: 0.8,
                  type: "spring",
                  stiffness: 200
                }}
                whileHover={{ 
                  rotate: [0, -10, 10, 0],
                  scale: 1.1,
                  boxShadow: "0 0 30px rgba(196, 211, 34, 0.5)"
                }}
              >
                {service.icon}
              </motion.div>
              
              <motion.h3 
                className="text-2xl font-bold text-white mb-4 text-center"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2 + 0.5, duration: 0.6 }}
              >
                {service.title}
              </motion.h3>
              <motion.p 
                className="text-gray-300 mb-6 text-center"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2 + 0.7, duration: 0.6 }}
              >
                {service.description}
              </motion.p>
              
              <motion.ul 
                className="space-y-3 mb-8"
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2 + 0.9, duration: 0.6 }}
              >
                {service.features.map((feature, idx) => (
                  <motion.li 
                    key={idx} 
                    className="flex items-center gap-3"
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.2 + 0.9 + idx * 0.1, duration: 0.4 }}
                  >
                    <motion.div 
                      className="w-2 h-2 bg-[#C4D322] rounded-full"
                      initial={{ scale: 0 }}
                      whileInView={{ scale: 1 }}
                      viewport={{ once: true }}
                      transition={{ 
                        delay: index * 0.2 + 0.9 + idx * 0.1,
                        duration: 0.3,
                        type: "spring",
                        stiffness: 300
                      }}
                    ></motion.div>
                    <span className="text-gray-300">{feature}</span>
                  </motion.li>
                ))}
              </motion.ul>
              
              <div className="text-center">
                <motion.div 
                  className="text-2xl font-bold text-[#C4D322] mb-4"
                  initial={{ opacity: 0, scale: 0.5 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ 
                    delay: index * 0.2 + 1.2,
                    duration: 0.6,
                    type: "spring",
                    stiffness: 200
                  }}
                >
                  {service.price}
                </motion.div>
                <motion.button
                  onClick={onOpenAppointment}
                  className="w-full py-3 bg-gradient-to-r from-[#C4D322] to-[#A8B91A] text-[#181818] font-bold rounded-lg hover:shadow-xl hover:shadow-[#C4D322]/20 transition-all duration-300"
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.2 + 1.4, duration: 0.6 }}
                  whileHover={{ 
                    scale: 1.05,
                    boxShadow: "0 10px 30px rgba(196, 211, 34, 0.3)"
                  }}
                  whileTap={{ scale: 0.95 }}
                >
                  Get Started Today
                </motion.button>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

// CTA Section
const CTASection = ({ onOpenAppointment }) => (
  <section className="py-20 bg-[#181818] relative overflow-hidden">
    {/* Animated Background Elements */}
    <div className="absolute inset-0">
      <motion.div 
        className="absolute top-0 left-1/4 w-96 h-96 bg-[#C4D322]/10 rounded-full blur-3xl"
        animate={{
          x: [0, 100, -50, 0],
          y: [0, -50, 100, 0],
          scale: [1, 1.5, 0.8, 1],
        }}
        transition={{
          duration: 12,
          repeat: Infinity,
          repeatType: "reverse"
        }}
      ></motion.div>
      <motion.div 
        className="absolute bottom-0 right-1/4 w-96 h-96 bg-[#C4D322]/5 rounded-full blur-3xl"
        animate={{
          x: [0, -80, 120, 0],
          y: [0, 80, -40, 0],
          scale: [1, 0.6, 1.4, 1],
        }}
        transition={{
          duration: 15,
          repeat: Infinity,
          repeatType: "reverse"
        }}
      ></motion.div>
    </div>
    
    <div className="container mx-auto px-6 text-center relative z-10">
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="max-w-4xl mx-auto"
      >
        <motion.h2 
          className="text-4xl md:text-6xl font-bold text-white mb-6"
          initial={{ opacity: 0, scale: 0.5, rotateZ: -5 }}
          whileInView={{ opacity: 1, scale: 1, rotateZ: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, type: "spring", stiffness: 100 }}
        >
          Ready to{' '}
          <motion.span 
            className="text-transparent bg-clip-text bg-gradient-to-r from-[#C4D322] to-[#A8B91A]"
            initial={{ opacity: 0, rotateY: 180, scale: 0.3 }}
            whileInView={{ opacity: 1, rotateY: 0, scale: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.3, duration: 0.8, type: "spring", stiffness: 80 }}
          >
            Dominate
          </motion.span>{' '}
          Your Local Market?
        </motion.h2>
        
        <motion.p 
          className="text-xl text-gray-300 mb-8"
          initial={{ opacity: 0, y: 30, skewY: 3 }}
          whileInView={{ opacity: 1, y: 0, skewY: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.5, duration: 0.6 }}
        >
          Book your free strategy call and discover exactly how to double your membership in the next 6 months.
        </motion.p>
        
        <motion.div 
          className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-8"
          initial={{ opacity: 0, scale: 0.8 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.7, duration: 0.6 }}
        >
          <motion.button
            onClick={onOpenAppointment}
            className="px-10 py-4 bg-gradient-to-r from-[#C4D322] to-[#A8B91A] text-[#181818] font-bold text-xl rounded-lg hover:shadow-2xl hover:shadow-[#C4D322]/30 transition-all duration-300 transform hover:scale-105"
            whileHover={{ 
              scale: 1.08,
              rotate: [0, -1, 1, 0],
              boxShadow: "0 25px 50px -12px rgba(196, 211, 34, 0.4)"
            }}
            whileTap={{ scale: 0.95 }}
            animate={{
              y: [0, -8, 0],
              boxShadow: [
                "0 10px 30px rgba(196, 211, 34, 0.2)",
                "0 20px 60px rgba(196, 211, 34, 0.3)",
                "0 10px 30px rgba(196, 211, 34, 0.2)"
              ]
            }}
            transition={{
              y: {
                duration: 3,
                repeat: Infinity,
                repeatType: "reverse",
                ease: "easeInOut"
              },
              boxShadow: {
                duration: 3,
                repeat: Infinity,
                repeatType: "reverse",
                ease: "easeInOut"
              }
            }}
          >
            Book Your Free Strategy Call
          </motion.button>
        </motion.div>
        
        <motion.div 
          className="flex items-center justify-center gap-8 text-gray-400"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.9, duration: 0.6 }}
        >
          <motion.div 
            className="flex items-center gap-2"
            whileHover={{ scale: 1.1, color: "#C4D322" }}
            transition={{ duration: 0.3 }}
          >
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
            >
              <Award className="w-5 h-5 text-[#C4D322]" />
            </motion.div>
            <span>5+ Years Experience</span>
          </motion.div>
          <motion.div 
            className="flex items-center gap-2"
            whileHover={{ scale: 1.1, color: "#C4D322" }}
            transition={{ duration: 0.3 }}
          >
            <motion.div
              animate={{ 
                scale: [1, 1.2, 1],
                rotate: [0, 180, 360]
              }}
              transition={{ 
                duration: 2,
                repeat: Infinity,
                repeatType: "reverse"
              }}
            >
              <Zap className="w-5 h-5 text-[#C4D322]" />
            </motion.div>
            <span>90-Day Results Guarantee</span>
          </motion.div>
        </motion.div>
      </motion.div>
    </div>
  </section>
);

const FitnessLandingPage = () => {
  const [showAppointment, setShowAppointment] = React.useState(false);
  const [openAppointmentDirect, setOpenAppointmentDirect] = React.useState(false);

  const handleOpenAppointment = () => {
    setOpenAppointmentDirect(true);
    setShowAppointment(true);
  };

  return (
    <div className="min-h-screen bg-[#181818]">
      <HeroSection onOpenAppointment={handleOpenAppointment} />
      <PainPointsSection />
      <SoftSolutionsSection />
      <HardSellingSection onOpenAppointment={handleOpenAppointment} />
      <CTASection onOpenAppointment={handleOpenAppointment} />
      
      {showAppointment && (
        <TechryptChatbot
          isOpen={showAppointment}
          onClose={() => {
            setShowAppointment(false);
            setOpenAppointmentDirect(false);
          }}
          openAppointmentDirect={openAppointmentDirect}
          limitBotResponses={true}
        />
      )}
    </div>
  );
};

export default FitnessLandingPage;