import React from "react";
import Hero from "../../components/Hero/Hero";
import Payment from "../../components/Payment/Payment";
import ServicesComponent from "../../components/Services/Services";
import Design from "../../components/Design/Design";
import Awards from "../../components/Awards/Awards";
import BusinessVerticals from "../../components/BusinessVerticals/BusinessVerticals";
import AboutSlider from "../../components/AboutSlider/AboutSlider";


const Services = () => {
  return (
    <div style={{ background: "#0f0f0f" }} className="min-h-screen">
      <div className="container-responsive spacing-responsive-lg text-center">
        <h1 className="text-responsive-4xl md:text-6xl lg:text-7xl font-black text-white mb-8 md:mb-16 uppercase tracking-wider relative animate-fade-in">
          Services
          <span className="absolute -bottom-4 left-1/2 transform -translate-x-1/2 w-32 md:w-48 lg:w-56 h-1.5 bg-primary block animate-underline-grow"></span>
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
      <BusinessVerticals />
      <ServicesComponent />
      <Payment />
      <AboutSlider />
      <Design />
      <Awards />
    </div>
  );
};

export default Services;