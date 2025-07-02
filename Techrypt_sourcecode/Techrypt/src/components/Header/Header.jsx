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
    { id: "BlogPage", label: "Blogs", path: "/BlogPage" },
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
      {/* Enhanced Desktop Navbar - Only visible on screens */}
      <nav className="navbar hidden lg:flex" style={{  paddingTop: '0px'}}>
        <div className="leftNav overflow-hidden">
          <Link to="/" className="flex items-center">
            {/* Desktop logo - properly sized and aligned */}
            <video
              autoPlay
              loop
              muted
              src={HeaderLogo}
              alt="Techrypt Logo"
              className="w-32 h-14 object-cover"
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
            height: "100%", 
            
          }}
        >
          <ul
            className="navList"
            style={{
              display: "flex",
              listStyle: "none",
              padding: 0,
              margin: 0,
              alignItems: "center", 
            }}
          >

          <li className="relative listItems group">
          {/* Trigger button */}
          <div className="navButton cursor-pointer px-4 py-2 text-white">
            Verticals
          </div>

          {/* Dropdown */}
          <div className="absolute top-full left-0 w-56 bg-black rounded-xl shadow-lg opacity-0 group-hover:opacity-100 pointer-events-none group-hover:pointer-events-auto transition-opacity duration-200 z-50">
            {/* Invisible bridge to prevent gap */}
            <div className="h-2 -mt-2"></div>
            <Link
              to="/LandingPages/PetLandingPage"
              onClick={handleLinkClick}
              className="block px-4 py-3 text-white hover:bg-[#C4D322] rounded-t-xl transition-colors"
            >
              Pet Industry
            </Link>
            <Link
              to="/LandingPages/FitnessLandingPage"
              onClick={handleLinkClick}
              className="block px-4 py-3 text-white hover:bg-[#C4D322] rounded-b-xl transition-colors"
            >
              Fitness Industry
            </Link>
          </div>
        </li>

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
      <div className="small-nav lg:hidden">
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