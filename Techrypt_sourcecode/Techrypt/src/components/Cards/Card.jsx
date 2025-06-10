import React from "react";
import { work1, work2, work3 } from "../../assets/mainImages";

const Card = () => {
  // Sample data array - you can pass this as a prop or import from elsewhere
  const cardData = [
    {
      id: 1,
      image: work1,
      title: "Big Bite",
      description: "A mouthwatering journey through our viral burger campaign that increased sales by 300% with strategic social media placements",
      link: "#"
    },
    {
      id: 2,
      image: work2,
      title: "Barbie Lashes",
      description: "Transforming beauty standards with our pink-themed lash collection campaign that trended across 15 TikTok beauty communities",
      link: "#"
    },
    {
      id: 3,
      image: work3,
      title: "Keithson Burgers",
      description: "Rebranding a classic diner chain with our retro-futuristic visual campaign that revived their 80s heritage for Gen Z",
      link: "#"
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 mx-auto">
      {cardData.map((card) => (
        <div key={card.id} className="relative m-6 h-[600px] border-2 border-white rounded-[50px] group">
          {/* Background Image */}
          <div className="absolute inset-0 flex justify-center items-center bg-[#0f0f0f] rounded-[50px] transition-opacity duration-200">
            <div
              className="w-44 h-44 bg-center bg-cover bg-no-repeat rounded-full  group-hover:opacity-0 transition-opacity duration-200"
              style={{ backgroundImage: `url(${card.image})` }}
            >
              {/* <img
              src={card.image}
              alt={card.title}
              className="w-20 h-20 rounded-full  opacity-0 group-hover:opacity-100 transition-opacity duration-200" /> */}
            </div>
          </div>


          {/* Hover Content */}
          <div className="absolute inset-0 bg-[#0f0f0f] opacity-0 group-hover:opacity-100 transition-opacity duration-200 rounded-[50px] flex flex-col gap-5 items-center justify-center">
            <div className="text-center px-6 mt-[30%]">
              <h3 className="font-bold text-5xl leading-[3.4rem] tracking-tight glowing-green text-white">
                {card.title}
              </h3>
              <p className="mt-4 text-lg leading-[1.65rem] text-white">
                {card.description}
              </p>
            </div>
            <a
              href={card.link}
              className="mt-4 font-medium text-lg leading-[1.6rem] rounded-full text-white px-4 py-2 mx-auto bg-primary glow-hover"
            >
              Learn More
            </a>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Card;