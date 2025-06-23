import React, { useEffect, useState, useRef } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";
import "./App.css";
import CursorGradient from './components/CursorGradient/CursorGradient.jsx';

// Import components
import Footer from "./components/Footer/Footer.jsx";
import Header from "./components/Header/Header.jsx";
import MessageSidebar from "./components/MessageSidebar/MessageSidebar.jsx";

// Import pages
import Main from "./pages/Main/main.jsx";
import Influence from "./pages/Influence/influence.jsx";
import Creative from "./pages/Creative/creative.jsx";
import Services from "./pages/Services/services.jsx";
import Work from "./pages/Work/work.jsx";
import About from "./pages/About/About.jsx";
import EventCalendar from "./pages/EventCalendar/EventCalendar.jsx";
import Offers from "./pages/Offers/Offers.jsx";
import ContactPage from "./pages/ContactPage/ContactPage.jsx";
import VerticalsPage from "./pages/Verticals/verticals.jsx";
import PetLandingPage from "./pages/LandingPages/PetlandingPage.jsx";

// Import other components
import { AnimatedLoader } from "./assets/mainImages.js";
import { ToastContainer } from "react-toastify";
import PrivacyPolicy from "./components/PrivacyPolicy/PrivacyPolicy.jsx";
import TermsConditions from "./components/TermsConditions/TermsConditions.jsx";

// Scroll to top on route change
const ScrollToTop = () => {
  const location = useLocation();
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [location.pathname]);

  return null;
};

const AppContent = () => {
  const location = useLocation();
  const isFirstLoad = useRef(true);
  const [loader, setLoader] = useState(true);

  useEffect(() => {
    // Always show loader on route change
    setLoader(true);
    console.log(`🔄 Loading animation triggered for: ${location.pathname}`);

    const duration = isFirstLoad.current ? 3000 : 1500;
    console.log(`⏱️ Animation duration: ${duration}ms`);

    const timer = setTimeout(() => {
      console.log('✅ Animation complete, hiding loader');
      setLoader(false);
      if (isFirstLoad.current) {
        isFirstLoad.current = false;
      }
    }, duration);

    return () => clearTimeout(timer);
  }, [location.pathname]);

  return loader ? (
    <div className="flex justify-center items-center fixed inset-0 bg-[#000] z-[9999] p-4">
      <img src={AnimatedLoader} alt="Loading..." className="w-32 h-32 md:w-44 md:h-44 object-contain" />
    </div>
  ) : (
    <>
      {/*Unused gradient component*/} 
      {/*<CursorGradient />*/} 
      <ToastContainer toastClassName={"bg-[#121212] border-2 border-primary text-white"} progressClassName={"bg-primary"} />
      <ScrollToTop />
      <Header />
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/Influence" element={<Influence />} />
        <Route path="/Services" element={<Services />} />
        <Route path="/Performance" element={<Services />} /> {/* Redirect old Performance route to Services */}
        <Route path="/Creative" element={<Creative />} />
        <Route path="/Work" element={<Work />} />
        <Route path="/About" element={<About />} />
        <Route path="/Calendar" element={<EventCalendar />} />
        <Route path="/PrivacyPolicy" element={<PrivacyPolicy />} />
        <Route path="/Terms&Conditions" element={<TermsConditions />} />
        <Route path="/Offers" element={<Offers />} />
        <Route path="/Contact" element={<ContactPage />} />
        <Route path="/Verticals" element={<VerticalsPage />} />
        <Route path="/PetLandingPage" element={<PetLandingPage />} />
        {/* Add the correct route for the Header link */}
        <Route path="/LandingPages/PetLandingPage" element={<PetLandingPage />} />
      </Routes>
      <MessageSidebar />
      <Footer />
    </>
  );
};

const App = () => (
  <Router>
    <AppContent />
  </Router>
);

export default App;