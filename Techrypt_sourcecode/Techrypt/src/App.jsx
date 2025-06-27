import React, { useEffect, useState, useRef } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
  Navigate,
} from "react-router-dom";
import "./App.css";
import CursorGradient from './components/CursorGradient/CursorGradient.jsx';
import { AuthProvider } from './context/AuthContext.jsx';

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
import PRLandingPage from "./pages/LandingPages/PRLandingPage.jsx";
import BlogPage from "./pages/BlogPage/BlogPage.jsx";
import BlogDetailPage from "./pages/BlogPage/BlogDetailPage.jsx";
import AdminDashboard from "./pages/AdminDashboard/AdminDashboard.jsx";
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
  const isAdminRoute = location.pathname.toLowerCase().startsWith('/admin');
  const isFirstLoad = useRef(true);
  const [loader, setLoader] = useState(true);

  useEffect(() => {
    // Only run this once on mount
    const timer = setTimeout(() => setLoader(false), 1500); // or however long you want
    return () => clearTimeout(timer);
  }, []); 

  if (loader) {
    return (
      <div className="flex justify-center items-center fixed inset-0 bg-[#000] z-[9999] p-4">
        <img src={AnimatedLoader} alt="Loading..." className="w-32 h-32 md:w-44 md:h-44 object-contain" />
      </div>
    );
  }

  return (
    <>
      {/*Unused gradient component*/} 
      {/*<CursorGradient />*/} 
      <ToastContainer toastClassName={"bg-[#121212] border-2 border-primary text-white"} progressClassName={"bg-primary"} />
      <ScrollToTop />
      
      {/* Only show header on non-admin routes */}
      {!isAdminRoute && <Header />}
      
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/Influence" element={<Influence />} />
        <Route path="/Services" element={<Services />} />
        <Route path="/Performance" element={<Services />} /> 
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
        <Route path="/LandingPages/PetLandingPage" element={<PetLandingPage />} />
        <Route path="/LandingPages/PRLandingPage" element={<PRLandingPage />} />
        <Route path="/BlogPage" element={<BlogPage />} />
        <Route path="/blog" element={<BlogPage />} />
        <Route path="/blog/:id" element={<BlogDetailPage />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/Admin/*" element={<AdminDashboard />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      
      {/* Only show message sidebar and footer on non-admin routes */}
      {!isAdminRoute && <MessageSidebar />}
      {!isAdminRoute && <Footer />}
    </>
  );
};

const App = () => (
  <Router>
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  </Router>
);

export default App;