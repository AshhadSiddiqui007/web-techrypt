import React from "react";
import Hero from "../../components/Hero/Hero";
import OtherWorks from "../../components/OtherWorks/OtherWorks";

const work = () => {
  return (
    <>
      <div style={{ backgroundColor: "#0f0f0f" }}>
        <Hero title={["Our", "Portfolio", "Showcase"]} text={"Discover our latest projects and success stories across various industries."} />
        <div className="fading"></div>
        <OtherWorks />
      </div>
    </>
  );
};

export default work;
