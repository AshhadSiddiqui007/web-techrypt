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
    <div style={{ background: "#0f0f0f" }}>
      <Hero text={"Comprehensive digital solutions tailored to your business needs — from website development to AI-powered automation."} />
      <div className="fading"></div>
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
