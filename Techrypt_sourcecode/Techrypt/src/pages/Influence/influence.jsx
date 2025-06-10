import React from "react";
import Hero from "../../components/Hero/Hero";
import Pricing from "../../components/Pricing/Pricing";
import Verticals from "../../components/Verticals/Verticals";
import InfluencerAndPlatforms from "../../components/InfluencerAndPlatforms/InfluencerAndPlatforms";

const influence = () => {
  return (
    <>
      <div
        style={{
          background: "#0f0f0f",
        }}
      >
        <Hero />
        <div className="fading"></div>
        <InfluencerAndPlatforms />
        <Pricing />
      </div>
    </>
  );
};
export default influence;
