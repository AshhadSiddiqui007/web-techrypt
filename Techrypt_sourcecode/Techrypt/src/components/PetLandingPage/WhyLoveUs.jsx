import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { MessageCircle, Calendar, Globe } from 'lucide-react';

const WhyLoveUs = ({ fadeInUp, staggerContainer }) => {
  useEffect(() => {
    // Animation control based on page visibility
    if(typeof document.hidden !== "undefined") {
      function animationRun(){
        const domSwing = document.getElementById('swinging');
        const domShadow = document.getElementById('shadow-anim');
        
        if (domSwing && domShadow) {
          if (document.hidden) {
            domSwing.style.animationPlayState = "paused";
            domShadow.style.animationPlayState = "paused";
          } else {
            domSwing.style.animationPlayState = "running";
            domShadow.style.animationPlayState = "running";
          }
        }
      }
      
      document.addEventListener('visibilitychange', animationRun, false);
      
      // Cleanup
      return () => {
        document.removeEventListener('visibilitychange', animationRun, false);
      };
    }
  }, []);

  const features = [
    {
      icon: MessageCircle,
      title: "24/7 AI Chatbot",
      description: "Never miss a customer inquiry. Our AI responds instantly, books appointments, and answers questions around the clock."
    },
    {
      icon: Calendar,
      title: "Automated Booking System",
      description: "Smart scheduling that prevents double-bookings, sends reminders, and optimizes your calendar for maximum revenue."
    },
    {
      icon: Globe,
      title: "Multilingual Client Support",
      description: "Serve customers in their preferred language. Our AI speaks 50+ languages fluently and culturally adapts responses."
    }
  ];

  return (
    <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-dark-lighter/50">
      <style jsx>{`
        .cat-animation-container {
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .cat-svg {
          display: inline-block;
          vertical-align: middle;
          width: 60%;
          max-width: 300px;
          min-width: 200px;
        }

        .cat-replacement {
          fill: #C4D322;
        }

        .swing {
          fill: #ffffff;
        }

        #swinging {
          transform-origin: top center;
          animation: swingme 2s ease-in-out 0s infinite;
        }

        @keyframes swingme {
          0%, 100% {
            transform: rotate(10deg);
          }
          50% {
            transform: rotate(-10deg);
          }
        }

        #shadow-anim {
          fill: #000;
          fill-opacity: 0.2;
          animation: shadow 2s ease-in-out 0s infinite;
        }

        @keyframes shadow {
          0%, 100% {
            transform: translateX(-2em);
          }
          50% {
            transform: translateX(2em);
          }
        }

        .loading-text {
          font-family: 'Inter', sans-serif;
          font-size: 24px;
          font-weight: bold;
          font-style: italic;
          fill: #C4D322;
          color: #C4D322;
        }

        @media (max-width: 768px) {
          .cat-svg {
            width: 70%;
            min-width: 180px;
          }
          .loading-text {
            font-size: 18px;
          }
        }
      `}</style>

      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl lg:text-5xl font-bold mb-6">
            Why Pet Businesses{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">
              Love Us
            </span>
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Transform your pet grooming business with AI that never sleeps, never forgets, and always upsells.
          </p>
        </motion.div>

        <motion.div
          variants={staggerContainer}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true }}
          className="grid lg:grid-cols-2 gap-12 items-center"
        >
          {/* Left column - Cat animation */}
          <motion.div 
            variants={fadeInUp}
            className="relative cat-animation-container"
          >
            <svg className="cat-svg" viewBox="0 0 346 512" version="1.1" role="img">
              <title>Pet Business Loading</title>
              <desc>A cat swinging gently on a swing representing automated pet business</desc>
              <g id="swinging">
                {/* Cat SVG embedded where the chicken used to be */}
                <g transform="translate(450, 50) scale(0.3)">
                  <path className="cat-replacement" d="M-827.3,979.5c0,0-2.2-13.1-5.2-17.1c-3.8-5.1-16.4-12.1-16.4-12.1c-2.6,3.7,3.6-9.8,7.3-22.7c0,0-24.2,3.2-46.8,27.6
                    c-6.4,7-17.8,38.6-17.8,38.6l-44.7,20.5c-31.1,12.9-82.7,26.2-82.7,97.7v30.5c-2.5-1.7-15.7-12.7-15.5-29.9
                    c0.1-13.6,1.9-27.5,3.6-39.9c3.1-22.7,5.5-47.1-3.7-57.6c-4.2-4.8-10.2-7.3-17.7-7.3c-4.9,0-8.9,4-8.9,8.9c0,4.9,4,8.9,8.9,8.9
                    c2.2,0,3.6,0.4,4.3,1.2c3.8,4.4,1.5,28.1-0.6,43.4c-1.7,12.9-3.7,27.5-3.7,42.2c0,16.2,5.6,31.4,15.7,42.8
                    c11.5,12.9,27.7,19.7,46.8,19.7c0,0,0,0,0,0h62.5h8.9h17.9c4.9,0,8.9-4,8.9-8.9s-4-8.9-8.9-8.9l-19.6,0l9.5-31.3
                    c0-4.5-1-8.8-2.7-12.6c-7.1-12.1-19.9-19.6-34-19.6c-6.2,0-12,1.4-17.5,4.1l-2.9-5.8c6.4-3.2,13.2-4.8,20.4-4.8
                    c16.8,0,32.3,9.2,40.3,24l0,0l0,0c0,0,33.1,50.7,36.4,57.9c0,0.1,0.1,0.1,0.1,0.2c0.9,2.7,3.1,4.7,5.9,5.3c0.1,0,0.2,0,0.3,0.1
                    c0.5,0.1,0.9,0.3,1.4,0.3h9.8c4.4,0,8.1-3.6,8.1-8.1c0-4.4-3.6-8.1-8.1-8.1h0.2c0,0-26.6-47.4-21.4-64.2
                    c23.7-37.2,36.5-72.5,36.5-72.5c5.1-11.6,18.2-20.5,20-21.7c4-2.7,9.5-6.1,10-11.3C-822.2,986.7-826,981.7-827.3,979.5z"/>
                </g>
                <path id="swing" className="swing" d="M 173 383.6 L 173 384 L 182.5 402 L 162.5 402 L 172 384 L 172 383.9 C 172.2 383.8 172.5 383.7 172.7 383.7 L 173 383.6 ZM 187.4 402 L 175.8 381.9 C 176.7 381 177.2 379.9 176.9 379 C 176.7 378.1 176 377.5 175 377.2 L 175 8 L 170 8 L 170 377.8 C 168 378.8 166.7 380.5 167.1 382 C 167.2 382.6 167.6 383.1 168.3 383.5 L 157.6 402 L 148 402 L 148 409 L 197 409 L 197 402 L 187.4 402 Z"/>
              </g>
              <g id="shadow-anim">
                <path d="M 145 497.5 C 145 495 157.8 493 173.5 493 C 189.2 493 202 495 202 497.5 C 202 500 189.2 502 173.5 502 C 157.8 502 145 500 145 497.5 Z" />
              </g>
              <g id="frame">
                <path d="M 173 2 C 159.2 2 148.3 8.7 142.2 20.1 L 142 20 L 141.7 21.1 C 139.8 24.9 137.6 29 137.2 33.3 L 0.1 512 L 9 512 L 141.5 48 L 205 48 L 337.1 512 L 346 512 L 208.8 32.8 C 208.3 28.8 206.2 25.1 204.6 21.6 L 204.1 20 L 203.8 20.1 C 197.7 8.7 186.8 2 173 2 ZM 173 10.2 C 183.8 10.2 192.1 15.3 196.7 24.2 L 200.7 34.8 C 200.8 35.5 200.8 37 200.8 37 L 145.2 37 C 145.2 37 145.2 35.8 145.2 35.2 L 149.5 23.8 C 154.2 15.1 162.4 10.2 173 10.2 Z" className="swing"/>
              </g>
              <text className="loading-text" x="100" y="465" width="220">
                <tspan>Automating...</tspan>
              </text>
            </svg>
          </motion.div>

          {/* Right column - Feature boxes stacked vertically */}
          <motion.div
            variants={staggerContainer}
            className="space-y-6"
          >
            {features.map((feature, index) => (
              <motion.div
                key={index}
                variants={fadeInUp}
                whileHover={{ x: 10, transition: { duration: 0.3 } }}
                className="bg-gradient-to-br from-dark-lighter to-dark-light rounded-2xl p-6 border border-dark-light hover:border-primary/50 transition-all duration-300 group"
              >
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform duration-300">
                    <feature.icon className="w-6 h-6 text-dark" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold mb-2 group-hover:text-primary transition-colors">
                      {feature.title}
                    </h3>
                    <p className="text-gray-300 leading-relaxed">
                      {feature.description}
                    </p>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
};

export default WhyLoveUs;