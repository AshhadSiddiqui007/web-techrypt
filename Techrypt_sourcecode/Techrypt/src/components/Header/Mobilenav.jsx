// Mobile Navigation Component
import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import "./Mobilenav.css";

const Mobilenav = () => {
    const location = useLocation();
    const [activeTab, setActiveTab] = useState("");
    const [showServicesDropdown, setShowServicesDropdown] = useState(false);
    
    const tabs = [
        { id: "services", label: "Services", path: "/Services" },
        { id: "portfolio", label: "Portfolio", path: "/Portfolio" },
        { id: "verticals", label: "Verticals", path: "/Verticals" },
        { id: "About", label: "About", path: "/About" },
        { id: "BlogPage", label: "Blogs", path: "/BlogPage" },
    ];

    useEffect(() => {
        // Set active tab based on current path
        const currentTab = tabs.find((tab) => location.pathname === tab.path);
        if (currentTab) {
            setActiveTab(currentTab.id);
        } else if (location.pathname === "/") {
            setActiveTab("");
        }
        // Check if we're on a vertical page
        if (location.pathname.includes("/LandingPages/")) {
            setActiveTab("verticals");
        }
    }, [location.pathname]);

    const handleTabClick = (tabId) => {
        setActiveTab(tabId);
        setShowServicesDropdown(false);
    };

    const toggleServicesDropdown = () => {
        setShowServicesDropdown(!showServicesDropdown);
    };

    return (
        <div className="influence-performance-container bg-primary py-1">
            <div className="tabs-wrapper">
                {/* Services tab with dropdown */}
                <div className="relative">
                    <button
                        className={`tab-button ${activeTab === "services" ? "text-primary bg-white" : "text-white"}`}
                        onClick={toggleServicesDropdown}
                    >
                        Services
                    </button>
                    
                    {/* Services Dropdown */}
                    {showServicesDropdown && (
                        <div className="absolute top-full left-0 w-48 bg-black rounded-lg shadow-lg z-50 mt-1">
                            <Link
                                to="/Services"
                                className="block px-4 py-2 text-white hover:bg-[#C4D322] rounded-t-lg transition-colors"
                                onClick={() => handleTabClick("services")}
                            >
                                All Services
                            </Link>
                            
                            {/* Verticals section */}
                            <div className="border-t border-gray-600">
                                <div className="px-4 py-2 text-gray-400 text-sm">Verticals:</div>
                                <Link
                                    to="/LandingPages/PetLandingPage"
                                    className="block px-4 py-2 text-white hover:bg-[#C4D322] transition-colors text-sm"
                                    onClick={() => handleTabClick("verticals")}
                                >
                                    Pet Industry
                                </Link>
                                <Link
                                    to="/LandingPages/FitnessLandingPage"
                                    className="block px-4 py-2 text-white hover:bg-[#C4D322] rounded-b-lg transition-colors text-sm"
                                    onClick={() => handleTabClick("verticals")}
                                >
                                    Fitness Industry
                                </Link>
                            </div>
                        </div>
                    )}
                </div>

                {/* Other tabs (excluding services and verticals since they're handled above) */}
                {tabs
                    .filter(tab => tab.id !== "services" && tab.id !== "verticals")
                    .map((tab) => (
                        <Link
                            to={tab.path}
                            key={tab.id}
                            className={`tab-button ${activeTab === tab.id ? "text-primary bg-white" : "text-white"}`}
                            onClick={() => handleTabClick(tab.id)}
                        >
                            {tab.label}
                        </Link>
                    ))}
            </div>
        </div>
    );
};

export default Mobilenav;