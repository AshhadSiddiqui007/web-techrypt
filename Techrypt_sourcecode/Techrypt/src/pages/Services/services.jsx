import React, { useState, useEffect } from "react";
import ServiceHero from "../../components/Services/ServiceHero";
import ServiceSection from "../../components/Services/ServiceSection";
import ServiceCTA from "../../components/Services/ServiceCTA";

const Services = () => {
  return (
    <div className="min-h-screen bg-black">
      <ServiceHero />
      <ServiceSection />
      <ServiceCTA />
    </div>
  );
};

export default Services;