import React from 'react';
import './FoldedCornerCard.css';

const VerticlesCard = ({ children, className = '', foldSize = 20, ...props }) => {
  return (
    <div
      className={`rounded-2xl  shadow-lg folded-corner-card ${className}`}
      style={{ '--fold-size': `${foldSize}px` }}
      {...props}
    >
      {children}
      <div className="folded-corner "></div>
    </div>
  );
};

export default VerticlesCard;