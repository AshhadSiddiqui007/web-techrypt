import "./Slider.css";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import content1 from "../../assets/svgs/content1.svg";
import content2 from "../../assets/svgs/content2.svg";
import content3 from "../../assets/svgs/content3.svg";
import content4 from "../../assets/svgs/content4.svg";
import content5 from "../../assets/svgs/content5.svg";
import content6 from "../../assets/svgs/content6.svg";
import content7 from "../../assets/svgs/content7.svg";
import content8 from "../../assets/svgs/content8.svg";
import content9 from "../../assets/svgs/content9.svg";
import content10 from "../../assets/svgs/content10.svg";
import content11 from "../../assets/svgs/content11.svg";
import content12 from "../../assets/svgs/content12.svg";
import content13 from "../../assets/svgs/content13.svg";
import content14 from "../../assets/svgs/content14.svg";
import content15 from "../../assets/svgs/content15.svg";
import mask from "../../assets/svgs/mask.svg";
import mask1 from "../../assets/svgs/mask1.svg";
import React from "react";
import Slider from "react-slick";

const sliderdata = [
  { maskImg: mask, logo: content1 },
  { maskImg: mask1, logo: content2 },
  { maskImg: mask, logo: content3 },
  { maskImg: mask1, logo: content4 },
  { maskImg: mask, logo: content5 },
  { maskImg: mask, logo: content6 },
  { maskImg: mask1, logo: content7 },
  { maskImg: mask, logo: content8 },
  { maskImg: mask1, logo: content9 },
  { maskImg: mask, logo: content10 },
  { maskImg: mask, logo: content11 },
  { maskImg: mask1, logo: content12 },
  { maskImg: mask, logo: content13 },
  { maskImg: mask1, logo: content14 },
  { maskImg: mask, logo: content15 },
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

  const leftToRightSettings = { ...baseSettings };

  const rightToLeftSettings = {
    ...baseSettings,
    rtl: true,
  };

  return (
    <div className="slider-main-container">
      <Slider {...leftToRightSettings}>
        {sliderdata.map((item, i) => (
          <div key={i} className="slider-container">
            <div className="slider-image-container">
              <img src={item?.logo} alt="logo" className="slider-image glowing-green" />
            </div>
          </div>
        ))}
      </Slider>

      <Slider {...rightToLeftSettings}>
        {sliderdata.map((item, i) => (
          <div key={i} className="slider-container">
            <div className="slider-image-container">
              <img src={item?.logo} alt="logo" className="slider-image glowing-green" />
            </div>
          </div>
        ))}
      </Slider>
    </div>
  );
}

export default AutoSlider;
