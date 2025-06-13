import "./Slider.css";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import React from "react";
import Slider from "react-slick";
import { motion } from "framer-motion";


import bbqbarn from "/Images/clients/bbqbarn.jpg";
import bolt from "/Images/clients/bolt.jpg";
import echoverse from "/Images/clients/echoverse.jpg";
import jazzybarbershop from "/Images/clients/jazzybarbershop.jpg";
import montoyacrew from "/Images/clients/montoyacrew.jpg";
import prx from "/Images/clients/prx.jpg";
import racksgangapparel from "/Images/clients/racksgangapparel.jpg";
import rooftobasement from "/Images/clients/rooftobasement.jpg";
import simonnicholas from "/Images/clients/simonnicholas.jpg";
import toothmechanic from "/Images/clients/toothmechanic.jpg";


const sliderdata = [
  { maskImg: bbqbarn, logo: bbqbarn },
  { maskImg: montoyacrew, logo: montoyacrew },
  { maskImg: echoverse, logo: echoverse },
  { maskImg: prx, logo: prx },
  { maskImg: bolt, logo: bolt },
  { maskImg: jazzybarbershop, logo: jazzybarbershop },
  { maskImg: rooftobasement, logo: rooftobasement },
  { maskImg: bbqbarn, logo: bbqbarn },  
  { maskImg: racksgangapparel, logo: racksgangapparel },
  { maskImg: toothmechanic, logo: toothmechanic },
  { maskImg: simonnicholas, logo: simonnicholas },

];

function AutoSlider() {
  const baseSettings = {
    infinite: true,
    slidesToShow: 5,
    slidesToScroll: 1,
    autoplay: true,
    speed: 2000,
    autoplaySpeed: 0,
    cssEase: "linear",
    arrows: false,
  };

  return (
    <div className="slider-main-container">
      <motion.h1
        className="text-white text-5xl md:text-6xl font-bold text-center mb-12"
        initial={{ opacity: 0, y: -20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.8 }}
      >
        Our Clients
      </motion.h1>
      <Slider {...baseSettings}>
        {sliderdata.map((item, i) => (
          <div key={i} className="slider-container">
            <div className="slider-image-container">
              {/* Using the imported image variables here */}
              <img src={item.logo} alt="logo" className="slider-image glowing-green" />
            </div>
          </div>
        ))}
      </Slider>
    </div>
  );
}

export default AutoSlider;
