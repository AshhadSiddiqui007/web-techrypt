import React, { useState } from 'react';

const DropdownMenu = ({ title, children }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleDropdownMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="dropdown-container" style={{ position: 'relative', display: 'inline-block' }}>
      <button 
        onClick={toggleDropdownMenu} 
        className="dropdown-toggle"
        style={{
          background: 'none',
          border: 'none',
          color: 'white',
          cursor: 'pointer',
          padding: '8px 16px',
          fontSize: '16px'
        }}
      >
        {title}
      </button>
      {isOpen && (
        <div 
          className="dropdown-content"
          style={{
            position: 'absolute',
            top: '100%',
            left: 0,
            backgroundColor: '#1a1a1a',
            minWidth: '200px',
            boxShadow: '0px 8px 16px 0px rgba(0,0,0,0.2)',
            zIndex: 1000,
            borderRadius: '4px',
            padding: '8px 0'
          }}
        >
          <div style={{ padding: '8px 16px' }}>
            {children}
          </div>
        </div>
      )}
    </div>
  );
};

export default DropdownMenu;