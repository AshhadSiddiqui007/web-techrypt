import React from "react";
import "./Pricing.css";

const Pricing = () => {
  const services = [
    {
      title: "Influencer Marketing",
      description: "Ad integration with influencers according to a standard video script",
      list: [
        "Dedicated specialist",
        "Brief creation and its localization",
        "Media planning",
        "Legal & financial supervising",
        "Advertising execution",
        "Post-campaign reporting",
      ],
      price: "$500",
    },
    {
      title: "Influencer Marketing 2.0",
      description: "Engaging content based on strategic and creative research",
      list: [
        "Dedicated team",
        "Brief creation and its localization",
        "Strategy research",
        "Competitor analysis",
        "Creative ideas generation",
        "Media planning",
        "Legal & financial supervising",
        "Advertising execution",
      ],
      price: "$1000",
    },
    {
      title: "Brand Awareness Campaigns",
      description: "Special projects and collaborations others will be jealous of",
      list: [
        "Dedicated team",
        "Brief creation and its localization",
        "Strategy research",
        "Competitor analysis",
        "Big idea generation",
        "Creative mechanics (collabs, giveaways, offline activities)",
        "Additional marketing services (UA, content production, web design, widgets, etc.)",
      ],
      price: "$1500",
    },
  ];

  return (
    <div className="marketing-container">
      {services.map((service, index) => (
        <div key={index} className="marketing-card">
          <h1>{service.title}</h1>
          <p>{service.description}</p>
          <ul>
            {service.list.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
          <div className="bottom-container">
            <span className="price-tag">{service.price}</span>
            <button className="buy-btn">Buy Now</button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Pricing;
