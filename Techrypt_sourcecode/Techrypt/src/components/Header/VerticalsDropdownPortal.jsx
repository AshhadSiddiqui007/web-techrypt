import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom";
import { Link } from "react-router-dom";

export default function VerticalsDropdownPortal({ anchorRef, open, onClose }) {
  const [style, setStyle] = useState({});

  useEffect(() => {
    if (open && anchorRef.current) {
      const rect = anchorRef.current.getBoundingClientRect();
      setStyle({
        position: "absolute",
        top: rect.bottom + window.scrollY,
        left: rect.left + window.scrollX,
        minWidth: rect.width,
        zIndex: 2000,
      });
    }
  }, [open, anchorRef]);

  if (!open) return null;

  return ReactDOM.createPortal(
    <div
      className="dropdown-content"
      style={style}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
    >
      <Link
        to="/LandingPages/PetLandingPage"
        className="block px-4 py-3 text-white hover:bg-[#C4D322] hover:text-black transition-colors"
      >
        Pet Industry
      </Link>
      <Link
        to="/LandingPages/FitnessLandingPage"
        className="block px-4 py-3 text-white hover:bg-[#C4D322] hover:text-black transition-colors"
      >
        Fitness Industry
      </Link>
    </div>,
    document.getElementById("dropdown-portal-root")
  );
}