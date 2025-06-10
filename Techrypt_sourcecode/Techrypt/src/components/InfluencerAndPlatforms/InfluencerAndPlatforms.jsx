import React from "react";
import "./InfluencerAndPlatforms.css";
import { social } from "../../assets/Data/Data";

export default function InfluencerAndPlatforms({ text }) {
  const socialClasses = [
    "youtube",
    "insta",
    "TikTok",
    "telegram",
    "twitch",
    "snap",
    "fbgaming",
    "podcast",
  ];

  return (
    <>
      <div className="Influencer">
        <h1 className="influence-h1">Any influencer, any platform</h1>

        <div className="Influencer-grid">
          {social.map((item, i) => (
            <div className={`grid-cards ${socialClasses[i]}`} key={i}>
              <img src={item?.icon} alt="logo" className="slider-image" />
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
