import React from "react";
import Hero from "../../components/Hero/Hero";
import Payment from "../../components/Payment/Payment";
import Services from "../../components/Services/Services";
import Design from "../../components/Design/Design";
import Awards from "../../components/Awards/Awards";

const performance = () => {
  return (
    <div style={{ background: "#0f0f0f" }}>
      <Hero text={"Innovative strategies, real results — every service at Techrypt is performance-driven and outcome-focused."} />
      <div className="fading"></div>
      <Payment />
      <Services />
      <Design />
      <Awards />
    </div>
  );
};

export default performance;
