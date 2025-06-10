import React, { useEffect, useState, useRef } from "react";
import "./Hero.css";
import video from "../../assets/heroBgVideo.mp4";

const Hero = ({ text, still = false, title = ["Development", "Branding", "Marketing"] }) => {
  const [currentText, setCurrentText] = useState(title[0]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFading, setIsFading] = useState(false);
  const videoRef = useRef(null);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setIsFading(true);
      if (!still) {
        setTimeout(() => {
          setCurrentIndex((prevIndex) => (prevIndex + 1) % title.length);
          setIsFading(false);
        }, 500);
      }

    }, 2000);

    return () => clearInterval(intervalId);
  }, []);

  useEffect(() => {
    if (!still) {
      setCurrentText(title[currentIndex]);
    }

  }, [currentIndex]);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.playbackRate = 0.5;
    }
  }, []);

  const handleVideoEnd = () => {
    videoRef.current.pause();
  };

  return (
    <div className="hero-section max-md:h-[70vh]">
      <video
        autoPlay
        muted
        loop
        className="absolute inset-0 w-full h-full object-cover opacity-50"
      >
        <source src={"https://jam3-media.imgix.net/uploads/2021/11/Jam3com-Reel-Nov102021-no-audio.mp4"} type="video/mp4" />
      </video>
      <div className="outer-headings ">
        <div className={` ${still ? "capitalize  mb-4 text-white font-semibold  text-2xl lg:text-5xl w-full md:w-[70%] overflow-visible" : "inner-headings"} ${isFading ? "fade-out" : "fade-in"}`}>
          <span>{currentText}</span>
        </div>
      </div>
      <div className="hero-para md:max-w-[800px] mx-auto text-center max-lg:pt-7 ">
        <p>{text}</p>
      </div>
      {/* <div className="smile"></div> */}
    </div>
  );
};

export default Hero;
