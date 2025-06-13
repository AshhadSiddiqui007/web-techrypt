import React, { useEffect, useState } from "react";
import "./Header.css";
import techryptLogo from "../../assets/Images/techryptLogo.jpeg";
import { Link, useLocation } from "react-router-dom";
import { HeaderLogo } from "../../assets/mainImages";
import ContactForm from "../ContactForm/ContactForm";

export default function Header() {
  const location = useLocation();
  const tabs = [
    { id: "services", label: "Services", path: "/Services" },
    { id: "work", label: "Work", path: "/Work" },
    { id: "verticals", label: "Verticals", path: "/Verticals" },
    { id: "About", label: "About", path: "/About" },
    { id: "Creative", label: "Creative", path: "/Creative" },
  ];
  const [activeTab, setActiveTab] = useState("");

  useEffect(() => {
    const currentTab = tabs.find((tab) => location.pathname === tab.path);
    if (currentTab) {
      setActiveTab(currentTab.id);
    } else if (location.pathname === "/") {
      setActiveTab("");
    }
    console.log("Current path:", location.pathname, "Active tab:", currentTab?.id);
  }, [location.pathname]);

  const handleLinkClick = () => {
    setActiveTab(""); // Reset active tab when link is clicked
  };

  return (
    <>
      {/* Desktop Navbar */}
      <nav className="navbar">
        <div className="leftNav overflow-hidden">
          <img src={techryptLogo} alt="" className="md:hidden" />
          <Link to="/" className="max-md:hidden">
            <video
              autoPlay
              loop
              muted
              src={HeaderLogo}
              alt=""
              className="icon object-cover w-[500px] lg:w-[300px]"
            />
          </Link>
          <hr className="hr1" />
        </div>

        <div
          className="midNav"
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            height: "100%", // Ensure the container takes full height
          }}
        >
          <ul
            className="navList"
            style={{
              display: "flex",
              listStyle: "none",
              padding: 0,
              margin: 0,
              alignItems: "center", // Vertically center the list items
            }}
          >
            {tabs.map((tab) => (
              <li className="listItems" key={tab.id}>
                <Link
                  to={tab.path}
                  className={`anchor navButton ${activeTab === tab.id ? "active" : ""}`}
                  onClick={(e) => {
                    setActiveTab(tab.id);
                    console.log(`Navigating to: ${tab.path}`);
                  }}
                >
                  {tab.label}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        <div className="rightNav">
          <hr className="hr2" />
          {/* Removed the hamburger menu button */}
        </div>
      </nav>

      {/* Mobile Navbar - Optional if you still want to keep a simpler mobile nav */}
      <div className="small-nav">
        <div className="leftNav">
          <a href="/">
            <img src={techryptLogo} alt="" width={100} className="icon" />
          </a>
        </div>
        <div className="linehor"></div>
        <div className="rightNav">
          {/* You can keep your mobile navigation here if you need it */}
        </div>
      </div>

      {/* Mobile Navigation Tabs - Only show on smaller screens */}
      <div className="mobile-nav-tabs">
        <div className="mobile-nav-container">
          <div className="mobile-tabs-wrapper">
            {tabs.map((tab) => (
              <Link
                to={tab.path}
                key={tab.id}
                className={`mobile-tab-button ${activeTab === tab.id ? "mobile-tab-active" : ""}`}
                onClick={(e) => {
                  setActiveTab(tab.id);
                  console.log(`Mobile navigating to: ${tab.path}`);
                }}
              >
                {tab.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
