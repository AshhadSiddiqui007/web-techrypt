import React from "react";
import Hero from "../../components/Hero/Hero";
import OtherWorks from "../../components/OtherWorks/OtherWorks";
import Filter from "../../components/Filter/Filter";

const work = () => {
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
          Our Work
          <span
            style={{
              color: "#a3d900",
              position: "absolute",
              bottom: "-15px",
              left: "50%",
              transform: "translateX(-50%)",
              width: "250px",
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
              100% { width: 250px; }
            }
          `}
        </style>
      </div>
      <Filter />
    </div>
  );
};

export default work;