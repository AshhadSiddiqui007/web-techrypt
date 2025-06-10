import React from "react";
import "./AboutWrite.css";
import { Link } from "react-router-dom";

export default function AboutWrite() {
  return (
    <>
      <div className="aboutwrite">
        <div className="aboutwrite-heading">
          <h1>They write about us</h1>
        </div>
        <div className="aboutwrite-content">
          <div className="content-rows">
            <h2>Automation for Growth</h2>
            <h2>AI Sales funnel</h2>
            <h2>Smart Cleint Booking</h2>
            <h2>Hands off Marketing</h2>
            <h2>Clinic Booking Automation</h2>

            <h2>Real Estate Bots</h2>
            <h2>Smart Service Delivery</h2>
            <h2>Tech Driven Scaling</h2>

            <h2>AI that Listens</h2>
            <h2>Ecommerce Sales Boost</h2>
            <h2>Smart Customer Intake</h2>
          </div>
        </div>
        <div className="aboutwrite-button bg-primary">
          <Link to={"/Work"}>Read our articles</Link>
        </div>
      </div>
    </>
  );
}
