import React, { useEffect, useState } from "react";
import "./Header.css";
import techryptLogo from "../../assets/Images/techryptLogo.png";
import { Link, useLocation } from "react-router-dom";
import { HeaderLogo } from "../../assets/mainImages";
import ContactForm from "../ContactForm/ContactForm";
import { HiMenu, HiX } from "react-icons/hi";
import DropdownMenu from "../DropDownMenu/DropDownMenu";
import TechryptChatbot from '../TechryptChatbot/TechryptChatbot';

export default function Header() {
  const location = useLocation();
  const tabs = [
    { id: "services", label: "Services", path: "/Services" },
    { id: "portfolio", label: "Portfolio", path: "/Portfolio" },
    { id: "verticals", label: "Verticals", path: "/Verticals" },
    { id: "About", label: "About", path: "/About" },
    { id: "BlogPage", label: "Blogs", path: "/BlogPage" },
    { id: "ContactUs", label: "Contact Us", path: "/Contact" },
  ];
  const [activeTab, setActiveTab] = useState("");
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isChatbotOpen, setIsChatbotOpen] = useState(false);
  const [openAppointmentDirect, setOpenAppointmentDirect] = useState(false);

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

  const openAppointmentForm = () => {
    setOpenAppointmentDirect(true);
    setIsChatbotOpen(true);
  };

  const closeChatbot = () => {
    setIsChatbotOpen(false);
    setOpenAppointmentDirect(false);
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

          {/* Services dropdown with nested Verticals */}
          <li className="relative listItems group">
            {/* Services trigger button */}
            <div className="navButton cursor-pointer px-4 py-2 text-white">
              Services
            </div>

            {/* Services Dropdown */}
            <div className="absolute top-full left-0 w-56 bg-black rounded-xl shadow-lg opacity-0 group-hover:opacity-100 pointer-events-none group-hover:pointer-events-auto transition-opacity duration-200 z-50">
              {/* Invisible bridge to prevent gap */}
              <div className="h-2 -mt-2"></div>
              
              <Link
                to="/Services"
                onClick={handleLinkClick}
                className="block px-4 py-3 text-white hover:bg-[#C4D322] rounded-t-xl transition-colors"
              >
                All Services
              </Link>
              
              {/* Nested Verticals dropdown */}
              <div className="relative group/nested">
                <div className="flex items-center justify-between px-4 py-3 text-white hover:bg-[#C4D322] transition-colors cursor-pointer">
                  <span>Verticals</span>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
                
                {/* Nested Verticals submenu */}
                <div className="absolute left-full top-0 w-56 bg-black rounded-xl shadow-lg opacity-0 group-hover/nested:opacity-100 pointer-events-none group-hover/nested:pointer-events-auto transition-opacity duration-200 z-50 -ml-2">
                  {/* Invisible bridge to prevent gap issues */}
                  <div className="absolute -left-2 top-0 w-2 h-full"></div>
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
              </div>
            </div>
          </li>

            {tabs
              .filter(tab => tab.id !== "verticals" && tab.id !== "services")
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
          
          {/* Book Demo Button */}
          <button
            onClick={openAppointmentForm}
            className="bg-[#c4d322] text-black font-semibold px-6 py-2 rounded-lg hover:bg-[#c4d322]/90 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl text-sm whitespace-nowrap mr-4"
          >
            Book Your Demo
          </button>
          
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
            {tabs
              .filter(tab => tab.id !== "ContactUs") // Add this filter to remove Contact Us from mobile tabs
              .map((tab) => (
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
              <Link
                to="/Services"
                className="mobile-menu-link touch-target"
                onClick={handleLinkClick}
              >
                Services
              </Link>
              
              {/* Verticals submenu items in mobile */}
              <div className="ml-4 border-l-2 border-gray-600 pl-4">
                <div className="text-gray-400 text-sm py-2 px-2">Verticals:</div>
                <Link
                  to="/LandingPages/PetLandingPage"
                  className="mobile-menu-link touch-target text-sm"
                  onClick={handleLinkClick}
                >
                  Pet Industry
                </Link>
                <Link
                  to="/LandingPages/FitnessLandingPage"
                  className="mobile-menu-link touch-target text-sm"
                  onClick={handleLinkClick}
                >
                  Fitness Industry
                </Link>
              </div>
              
              {tabs
                .filter(tab => tab.id !== "verticals" && tab.id !== "services" && tab.id !== "ContactUs")
                .map((tab) => (
                  <Link
                    key={tab.id}
                    to={tab.path}
                    className="mobile-menu-link touch-target"
                    onClick={handleLinkClick}
                  >
                    {tab.label}
                  </Link>
                ))}
              
              {/* Mobile Book Demo Button - Right above Contact Us */}
              <button
                onClick={() => {
                  openAppointmentForm();
                  setIsMobileMenuOpen(false); // Close menu when booking
                }}
                className="mobile-menu-link mobile-menu-cta touch-target bg-[#c4d322] text-black font-semibold hover:bg-[#c4d322]/90 transition-all duration-300"
              >
                Book Your Demo
              </button>
              
              {/* Keep this green Contact Us button */}
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

      {/* Add the TechryptChatbot component at the end, before closing </> */}
      <TechryptChatbot 
        isOpen={isChatbotOpen}
        onClose={closeChatbot}
        openAppointmentDirect={openAppointmentDirect}
      />
    </>
  );
}
