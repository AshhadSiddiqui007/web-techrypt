import React from "react";
import "./AboutAwards.css"; // Import the stylesheet

const awardsData = [
  {
    title: "Top Influencer Marketing Companies",
    organization: "Business of Apps",
  },
  {
    title: "Best UA & Advertising Finalist",
    organization: "Mobile Games Awards",
  },
  {
    title: "Most Innovative Campaign Finalist",
    organization: "Masterclassing Awards",
  },
  { title: "Global Leaders Awards", organization: "Clutch.co" },
  { title: "Top App Marketing Companies", organization: "Business of Apps" },
];

const AboutAwards = () => {
  return (
    <div className="awards-container">
      <h1 className="awards-title">Precious awards</h1>
      <div className="awards-list">
        {awardsData.map((award, index) => (
          <div className="award-item" key={index}>
            <div className="awardleft">
              <div className="award-title">{award.title}</div>
            </div>
            <div className="awardright">
              <div className="award-organization">{award.organization}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AboutAwards;
