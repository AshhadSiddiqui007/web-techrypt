import { useState, useEffect } from 'react';

const CursorGradient = () => {
  const [mousePosition, setMousePosition] = useState({ x: 50, y: 50 });

  useEffect(() => {
    const handleMouseMove = (e) => {
      const x = (e.clientX / window.innerWidth) * 100;
      const y = (e.clientY / window.innerHeight) * 100;
      setMousePosition({ x, y });
    };

    document.addEventListener('mousemove', handleMouseMove);
    return () => document.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <div
        className="fixed inset-0 pointer-events-none z-10 transition-all duration-100 ease-out"
        style={{
        background: `radial-gradient(200px circle at ${mousePosition.x}% ${mousePosition.y}%, 
        rgba(117, 211, 34, 0.6) 0%,   /* Reduced opacity */
        rgba(86, 163, 23, 0.6) 30%,  /* Reduced opacity */
        transparent 99%)`
        }}
    />

  );
};

export default CursorGradient;