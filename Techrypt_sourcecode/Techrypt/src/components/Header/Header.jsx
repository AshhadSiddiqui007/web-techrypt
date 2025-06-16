import React, { useEffect, useState } from "react";
import "./Header.css";
import techryptLogo from "../../assets/Images/techryptLogo.jpeg";
import { Link, useLocation } from "react-router-dom";
import { HeaderLogo } from "../../assets/mainImages";
import ContactForm from "../ContactForm/ContactForm";
import { HiMenu, HiX } from "react-icons/hi";

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
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

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
    setIsMobileMenuOpen(false); // Close mobile menu when link is clicked
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <>
      {/* Enhanced Desktop Navbar */}
      <nav className="navbar">
        <div className="leftNav overflow-hidden">
          <Link to="/" className="flex items-center">
            <img
              src={techryptLogo}
              alt="Techrypt Logo"
              className="md:hidden w-16 h-16 object-contain"
            />
            <video
              autoPlay
              loop
              muted
              src={HeaderLogo}
              alt="Techrypt Logo"
              className="hidden md:block icon object-cover w-[300px] lg:w-[250px] xl:w-[300px]"
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
          {/* Mobile Hamburger Menu Button */}
          <button
            className="md:hidden mobile-menu-button touch-target"
            onClick={toggleMobileMenu}
            aria-label="Toggle mobile menu"
          >
            {isMobileMenuOpen ? (
              <HiX className="text-white text-2xl" />
            ) : (
              <HiMenu className="text-white text-2xl" />
            )}
          </button>
        </div>
      </nav>

      {/* Enhanced Mobile Navbar */}
      <div className="small-nav">
        <div className="leftNav">
          <Link to="/" onClick={handleLinkClick}>
            <img
              src={techryptLogo}
              alt="Techrypt Logo"
              className="w-12 h-12 md:w-16 md:h-16 object-contain"
            />
          </Link>
        </div>
        <div className="linehor"></div>
        <div className="rightNav">
          <button
            className="mobile-menu-button touch-target"
            onClick={toggleMobileMenu}
            aria-label="Toggle mobile menu"
          >
            {isMobileMenuOpen ? (
              <HiX className="text-white text-xl" />
            ) : (
              <HiMenu className="text-white text-xl" />
            )}
          </button>
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

      {/* Mobile Menu Overlay */}
      {isMobileMenuOpen && (
        <div className="mobile-menu-overlay">
          <div className="mobile-menu-content">
            <div className="mobile-menu-header">
              <Link to="/" onClick={handleLinkClick}>
                <img
                  src={techryptLogo}
                  alt="Techrypt Logo"
                  className="w-16 h-16 object-contain"
                />
              </Link>
              <button
                className="mobile-menu-close touch-target"
                onClick={toggleMobileMenu}
                aria-label="Close mobile menu"
              >
                <HiX className="text-white text-2xl" />
              </button>
            </div>

            <nav className="mobile-menu-nav">
              {tabs.map((tab) => (
                <Link
                  key={tab.id}
                  to={tab.path}
                  className="mobile-menu-link touch-target"
                  onClick={handleLinkClick}
                >
                  {tab.label}
                </Link>
              ))}
              <Link
                to="/Contact"
                className="mobile-menu-link mobile-menu-cta touch-target"
                onClick={handleLinkClick}
              >
                Contact Us
              </Link>
            </nav>
          </div>
        </div>
      )}
    </>
  );
}
