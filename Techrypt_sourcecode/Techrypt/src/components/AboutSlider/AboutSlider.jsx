import React from "react";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import Slider from "react-slick";
import p1 from "../../assets/Images/applepodcasts.png";
import p2 from "../../assets/Images/facebookgaming.png";
import p3 from "../../assets/Images/instagram.png";
import p4 from "../../assets/Images/snapchat.png";
import p5 from "../../assets/Images/telegram.png";
import p6 from "../../assets/Images/tiktok.png";
import p7 from "../../assets/Images/twitch.png";
import p8 from "../../assets/Images/youtube.png";
import bmask1 from "../../assets/svgs/bmask1.svg";
import bmask2 from "../../assets/svgs/bmask2.svg";
import bmask5 from "../../assets/svgs/bmask5.svg";

export default function AboutSlider() {
  const aboutSliderData = [
    { logo: p1 },
    { logo: p2 },
    { logo: p3 },
    { logo: p4 },
    { logo: p5 },
    { logo: p6 },
    { logo: p7 },
    { logo: p8 },
  ];

  const settings = {
    infinite: true,
    slidesToShow: 4,
    slidesToScroll: 1,
    autoplay: true,
    speed: 2000,
    autoplaySpeed: 0,
    cssEase: "linear",
    arrows: false,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 1,
          infinite: true,
          dots: true,
        },
      },
      {
        breakpoint: 700,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1,
          initialSlide: 1,
        },
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
        },
      },
    ],
  };

  const getBackgroundImage = (index) => {
    if ((index + 1) % 3 === 1) return bmask1;
    if ((index + 1) % 3 === 2) return bmask2;
    return bmask5;
  };

  return (
    <div className="flex justify-center items-center bg-black pb-20">
      <div className="bg-primary rounded-[50px] w-[80vw] flex flex-col items-center justify-center p-5">
        <h1 className="text-[45px] text-blackS font-[450]">Certified By</h1>
        <div className="w-full mt-[10px]">
          <Slider {...settings}>
            {aboutSliderData.map((item, i) => (
              <div key={i} className="px-2">
                <div
                  className="relative flex justify-center items-center bg-no-repeat bg-center bg-contain h-[100px]"
                  style={{
                    backgroundImage: `url(${getBackgroundImage(i)})`
                  }}
                >
                  <img
                    src={item.logo}
                    alt="logo"
                    className="h-full w-auto"
                  />
                </div>
              </div>
            ))}
          </Slider>
        </div>
      </div>
    </div>
  );
}