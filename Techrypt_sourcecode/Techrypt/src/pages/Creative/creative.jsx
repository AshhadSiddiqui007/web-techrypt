import React from "react";
import Slider from "../../components/Slider/Slider";
import Content from "../../components/Contents/Content";
import Hero from "../../components/Hero/Hero";

const creative = () => {
  return (
    <>
      <div
        style={{
          background: "#0f0f0f",
        }}
      >
        <Hero text={"Where imagination meets execution — we bring ideas to life through design, code, and compelling stories."} />
        <div className="fading"></div>
        <Slider />
        <Content />
      </div>
    </>
  );
};

export default creative;
