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
    <div style={{ backgroundColor: "#0f0f0f" }}>
      <div
        style={{
          padding: "60px 20px",
          textAlign: "center",
        }}
      >
        <h1
          style={{
            fontSize: "64px",
            fontWeight: "900",
            color: "#ffffff",
            marginBottom: "60px",
            textTransform: "uppercase",
            letterSpacing: "3px",
            position: "relative",
            animation: "fadeIn 1.5s ease-in-out",
          }}
        >
          About Us
          <span
            style={{
              color: "#a3d900",
              position: "absolute",
              bottom: "-15px",
              left: "50%",
              transform: "translateX(-50%)",
              width: "240px",
              height: "6px",
              background: "#a3d900",
              display: "block",
              animation: "underlineGrow 1.5s ease-in-out",
            }}
          ></span>
        </h1>
        <style>
          {`
            @keyframes fadeIn {
              0% { opacity: 0; transform: translateY(20px); }
              100% { opacity: 1; transform: translateY(0); }
            }
            @keyframes underlineGrow {
              0% { width: 0; }
              100% { width: 240px; }
            }
          `}
        </style>
      </div>

      <AboutPara />

      {/* Move Plans (packages) section higher for better visibility */}
      <Plans />

      <AboutSlider />
      <ParallaxWrapper
        children={[
          <AboutCards />,
          <OurVision />,
        ]}
      />
      <ParallaxWrapper
        children={[
          <AboutWrite />,
        ]}
      />
      {/* <AboutAwards/> */}
    </div>
  );
};

export default About;