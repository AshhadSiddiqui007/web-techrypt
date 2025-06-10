import React, { useEffect, useState } from "react";
import "./Header.css";
import techryptLogo from "../../assets/Images/techryptLogo.jpeg";
import navIcon from "../../assets/svgs/close.svg";
import close from "../../assets/svgs/open.svg";
import { Link, useLocation } from "react-router-dom";
import { HeaderLogo } from "../../assets/mainImages";
import Mobilenav from "./Mobilenav";
import ContactForm from "../ContactForm/ContactForm";

export default function Header() {
  const location = useLocation()
  const tabs = [
    { id: "About", label: "About", path: "/About" },
    { id: "services", label: "Services", path: "/Services" },
    { id: "Creative", label: "Creative", path: "/Creative" },
    { id: "work", label: "Work", path: "/Work" },
  ];
  const [isDropdownVisible, setDropdownVisible] = useState(false);
  const [activeTab, setActiveTab] = useState("");
  useEffect(() => {
    // Set active tab based on current path
    const currentTab = tabs.find(tab => location.pathname === tab.path);
    if (currentTab) {
      setActiveTab(currentTab.id);
    } else if (location.pathname === '/') {
      setActiveTab(''); // Clear active tab for home page
    }
    console.log('Current path:', location.pathname, 'Active tab:', currentTab?.id);
  }, [location.pathname]);
  const toggleDropdown = () => {
    setDropdownVisible(!isDropdownVisible);
  };

  const handleLinkClick = () => {
    setDropdownVisible(false); // Hide dropdown on link click
  };

  return (
    <>
      {/* Desktop Navbar */}
      <nav className="navbar">
        <div className="leftNav overflow-hidden">
          <img src={techryptLogo} alt="" className="md:hidden" />
          <Link to="/" className="max-md:hidden">
            <video autoPlay loop muted src={HeaderLogo} alt="" className="icon object-cover w-[500px] lg:w-[300px] " />
          </Link>
          <hr className="hr1" />
        </div>

        <div className="midNav">
          <ul className="navList">
            {tabs.map((tab) => (
              <li className="listItems" key={tab.id}>
                <Link
                  to={tab.path}
                  className={`anchor navButton ${activeTab === tab.id ? "active" : ""}`}
                  onClick={(e) => {
                    // Don't prevent default - let React Router handle navigation
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
          <img
            src={isDropdownVisible ? close : navIcon}
            alt="navIcon"
            className="icon"
            onClick={toggleDropdown}
          />

          {/* Dropdown Menu */}
          {isDropdownVisible && (
            <div
              className={`dropdown ${isDropdownVisible ? "dropdown-visible" : "dropdown-hidden"
                }`}
            >
              <div className="yellowDiv glow-green">
                <ul className="navList">
                  <li className="dropDownList">
                    <Link
                      to="/Offers"
                      className="dropDownAnchor"
                      onClick={handleLinkClick}
                    >
                      Offers
                    </Link>
                  </li>
                  <li className="dropDownList">
                    <Link
                      to="/Calendar"
                      className="dropDownAnchor"
                      onClick={handleLinkClick}
                    >
                      Events Calendar
                    </Link>
                  </li>
                </ul>
              </div>

              <ContactForm />
              <div className="flex mt-4 flex-col md:flex-row gap-3 w-full justify-between items-start text-[#FFFFFF4D] footer-div  ">
                <p className="">
                  info@techrypt.io
                </p>
                <p className="md:w-95 text-center  max-md:order-3">
                  By clicking submit, you agree to our{" "}
                  <Link to="/PrivacyPolicy" className="  hover:text-[#ccc] transition-all duration-150">
                    Privacy Policy
                  </Link>{" "}
                  and{" "}
                  <Link to="/Terms&Conditions" className=" hover:text-[#ccc] transition-all duration-150">
                    Terms & Conditions
                  </Link>
                </p>
              </div>

            </div>
          )}
        </div>
      </nav>

      {/* Mobile Navbar */}
      <div className="small-nav">
        <div className="leftNav">
          <a href="/">
            <img src={techryptLogo} alt="" width={100} className="icon" />
          </a>
        </div>
        <div className="linehor"></div>
        <div className="rightNav">
          <img
            src={isDropdownVisible ? close : navIcon}
            alt="navIcon"
            className="icon"
            onClick={toggleDropdown}
          />
        </div>

        {/* Mobile Dropdown Menu */}
        {isDropdownVisible && (
          <div className="dropdown-mobile">
            <ul className="navList glow-green">
              {/* <li
                className="dropDownList"
                style={{
                  fontSize: "32px",
                  marginRight: "auto",
                }}
              >
                <Link to="/Influence" onClick={handleLinkClick}>
                  Influence
                </Link>
              </li> */}
              <li className="dropDownList" style={{ fontSize: "32px" }}>
                <Link to="/Calendar" onClick={handleLinkClick}>
                  Events Calendar
                </Link>
              </li>
            </ul>
            <div className="inputDiv">
              <div className="leftInput">
                <input type="text" placeholder="Your name" className="input" />
                <input type="text" placeholder="Your email" className="input" />
              </div>
              <div className="rightInput">
                <input
                  type="text"
                  placeholder="Your company name"
                  className="input"
                />
                <input
                  type="text"
                  placeholder="How did you hear about us?"
                  className="input"
                />
              </div>
            </div>
            <input
              type="text"
              placeholder="Your Goals / KPIs / Vision"
              className="Secondinput"
            />
            <button className="submit glow-hover">Submit</button>
          </div>
        )}
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
                  // Let React Router handle navigation
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
