import React, { useEffect, useState } from "react";
import "./Header.css";
import techryptLogo from "../../assets/Images/techryptLogo.png";
import { Link, useLocation } from "react-router-dom";
import { HeaderLogo } from "../../assets/mainImages";
import ContactForm from "../ContactForm/ContactForm";
import { HiMenu, HiX } from "react-icons/hi";
import DropdownMenu from "../DropDownMenu/DropDownMenu";

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
      {/* Enhanced Desktop Navbar - Only visible on screens >768px */}
      <nav className="navbar hidden md:flex" style={{ paddingTop: '10px' }}>
        <div className="leftNav overflow-hidden">
          <Link to="/" className="flex items-center">
            {/* Desktop logo - properly sized and aligned */}
            <video
              autoPlay
              loop
              muted
              src={HeaderLogo}
              alt="Techrypt Logo"
              className="desktop-header-logo icon object-cover"
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
           {/* Verticals dropdown with dual functionality */}
          <li className="listItems">
            <div className="dropdown-dual-function">
              <Link 
                to="/Verticals" 
                className={`anchor navButton ${activeTab === "verticals" ? "active" : ""}`}
                onClick={(e) => {
                  // Only set active tab if directly clicked (not when clicking a dropdown item)
                  if (e.currentTarget === e.target) {
                    setActiveTab("verticals");
                    console.log(`Navigating to: /Verticals`);
                  }
                }}
              >
                Verticals
              </Link>
              <div className="dropdown-content">
                <Link 
                  to="/LandingPages/PetLandingPage" 
                  onClick={handleLinkClick} 
                  style={{ color: 'white', textDecoration: 'none', display: 'block', padding: '10px 15px' }}
                >
                  Pet Landing Page
                </Link>
                {/* Add more landing pages here as needed */}
              </div>
            </div>
          </li>   

            {/* Render the rest of the tabs, excluding Verticals */}
            {tabs
              .filter(tab => tab.id !== "verticals")
              .map((tab) => (
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
          {/* Original Desktop Navigation Tabs */}
          <div className="hidden md:flex main-tabs">
            {tabs.map((tab) => (
              <Link
                key={tab.id}
                to={tab.path}
                className={`main-tab ${activeTab === tab.id ? "active" : ""}`}
                onClick={() => setActiveTab(tab.id)}
              >
                {tab.label}
              </Link>
            ))}
          </div>
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

      {/* Enhanced Mobile Navbar - Only visible on screens ≤768px */}
      <div className="small-nav md:hidden">
        <div className="leftNav">
          <Link to="/" onClick={handleLinkClick}>
            <video
              autoPlay
              loop
              muted
              playsInline
              src={HeaderLogo}
              alt="Techrypt Logo"
              className="w-24 h-8 object-contain"
              style={{
                maxWidth: '100%',
                height: 'auto'
              }}
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
                <video
                  autoPlay
                  loop
                  muted
                  playsInline
                  src={HeaderLogo}
                  alt="Techrypt Logo"
                  className="w-32 h-12 object-contain"
                  style={{
                    maxWidth: '100%',
                    height: 'auto'
                  }}
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