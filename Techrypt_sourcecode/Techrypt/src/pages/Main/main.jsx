import React from "react";
import Hero from "../../components/Hero/Hero";
import AgencyDetails from "../../components/AgencyDetails/AgencyDetails";
import SliderLogo from "../../components/SliderLogos/AutoSlider";
import CreativeTeamSection from "../../components/CreativeTeamSection/CreativeTeamSection.jsx";
import VideoGallery from "../../components/VideoGallery/VideoGallery.jsx";
import Verticals from "../../components/Verticals/Verticals.jsx";
import Services from "../../components/WhatWeDo/Services.jsx";
import ParallaxWrapper from "../../components/ParallaxWrapper/ParallaxWrapper.jsx";

const main = () => {
  return (
    <div className="relative">
      <Hero title={["Development", "Branding", "Marketing"]} text={" Unlock new opportunities with expert-led training & cutting-edge digital services. Techrypt.io is a forward-thinking team on a mission to revolutionize how individuals learn and how businesses grow."} />
      <div className="fading"></div>
      
      <AgencyDetails />
      <CreativeTeamSection />
      
      {/* <VideoGallery /> */}
      <SliderLogo />
      <Services className={"z-20"} />

      <Verticals />

    </div>
  );
};

export default main;
