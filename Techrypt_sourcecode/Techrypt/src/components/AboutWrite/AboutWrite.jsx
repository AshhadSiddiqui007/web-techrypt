import React from "react";
import "./AboutWrite.css";
import { Link } from "react-router-dom";

export default function AboutWrite() {
  const headings = [
    "Automation for Growth",
    "AI Sales funnel",
    "Smart Client Booking",
    "Hands off Marketing",
    "Clinic Booking Automation",
    "Real Estate Bots",
    "Smart Service Delivery",
    "Tech Driven Scaling",
    "AI that Listens",
    "Ecommerce Sales Boost",
    "Smart Customer Intake"
  ];

  return (
    <>
      <div className="aboutwrite">
        <div className="aboutwrite-heading">
          <h1>They write about us</h1>
        </div>
        <div className="aboutwrite-content">
          <div className="content-rows">
            {/* Desktop: Show all headings */}
            <div className="hidden md:block">
              {headings.map((heading, index) => (
                <h2 key={index}>{heading}</h2>
              ))}
            </div>
            
            {/* Mobile: Show only first 5 headings */}
            <div className="block md:hidden">
              {headings.slice(0, 5).map((heading, index) => (
                <h2 key={index}>{heading}</h2>
              ))}
            </div>
          </div>
        </div>
        <div className="aboutwrite-button bg-primary">
          <Link to={"/Work"}>Read our articles</Link>
        </div>
      </div>
    </>
  );
}