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
    <div className="hero-section h-screen md:h-screen mobile:h-[70vh] relative overflow-hidden">
      <video
        autoPlay
        muted
        loop
        className="absolute inset-0 w-full h-full object-cover opacity-50"
      >
        <source src={"https://jam3-media.imgix.net/uploads/2021/11/Jam3com-Reel-Nov102021-no-audio.mp4"} type="video/mp4" />
      </video>
      <div className="outer-headings relative z-10">
        <div className={`${still ?
          "capitalize mb-4 text-white font-semibold text-responsive-2xl lg:text-responsive-5xl w-full md:w-[70%] overflow-visible px-4 md:px-0" :
          "inner-headings text-responsive-4xl md:text-[145px]"
        } ${isFading ? "fade-out" : "fade-in"}`}>
          <span>{currentText}</span>
        </div>
      </div>
      <div className="hero-para max-w-[90%] md:max-w-[800px] mx-auto text-center px-4 md:px-0 pt-4 md:pt-7">
        <p className="text-responsive-base md:text-[25px]">{text}</p>
      </div>
    </div>
  );
};

export default Hero;
