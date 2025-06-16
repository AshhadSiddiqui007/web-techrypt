import React from "react";
import AboutPara from "../../components/AboutPara/AboutPara";
import AboutWrite from "../../components/AboutWrite/AboutWrite";
import AboutSlider from "../../components/AboutSlider/AboutSlider";
import Hero from "../../components/Hero/Hero";
import AboutAwards from "../../components/AboutAwards/AboutAwards";
import Plans from "../../components/Plans/Plans";
import AboutCards from "../../components/AboutCards/AboutCards";
import OurVision from "../../components/OurVision/OurVision";
import ParallaxWrapper from "../../components/ParallaxWrapper/ParallaxWrapper";

const About = () => {
  return (
    <div style={{ backgroundColor: "#0f0f0f" }} className="min-h-screen">
      <div className="container-responsive spacing-responsive-lg text-center">
        <h1 className="text-responsive-4xl md:text-6xl lg:text-7xl font-black text-white mb-8 md:mb-16 uppercase tracking-wider relative animate-fade-in">
          About Us
          <span className="absolute -bottom-4 left-1/2 transform -translate-x-1/2 w-32 md:w-48 lg:w-60 h-1.5 bg-primary block animate-underline-grow"></span>
        </h1>
        <style>
          {`
            @keyframes fadeIn {
              0% { opacity: 0; transform: translateY(20px); }
              100% { opacity: 1; transform: translateY(0); }
            }
            @keyframes underlineGrow {
              0% { width: 0; }
              100% { width: 100%; }
            }
            .animate-fade-in {
              animation: fadeIn 1.5s ease-in-out;
            }
            .animate-underline-grow {
              animation: underlineGrow 1.5s ease-in-out;
            }
          `}
        </style>
      </div>

      <AboutPara />
      <OurVision />,
      
     
      <ParallaxWrapper
        children={[
          <AboutCards />,
          
        ]}
      />
       <AboutSlider />
      <ParallaxWrapper
        children={[
          <AboutWrite />,
        ]}
      />
      <Plans />
    </div>
  );
};

export default About;