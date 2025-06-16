import React, { useRef, useState } from "react";
import "./VideoGallery.css";
import video1 from "../../assets/videos/feroze.mp4";
import video2 from "../../assets/videos/andra.mp4";
import video3 from "../../assets/videos/bohemia.mp4";
import video4 from "../../assets/videos/farhan.mp4";
import "@fortawesome/fontawesome-free/css/all.min.css";

const videoData = [
  {
      id: 1,
      title: "Social Media Marketing",
      url: video1,
      thumbnail: "https://via.placeholder.com/300x200.png?text=Intro+to+React",
    },
    {
      id: 2,
      title: "Bussiness Development Manager",
      url: video2,
      thumbnail: "https://via.placeholder.com/300x200.png?text=JavaScript+Basics",
    },
    {
      id: 3,
      title: "Account & Finance",
      url: video3,
      thumbnail: "https://via.placeholder.com/300x200.png?text=CSS+Flexbox+Guide",
    },
    {
      id: 4,
      title: "Human Resources Manager",
      url: video4,
      thumbnail:
        "https://via.placeholder.com/300x200.png?text=Understanding+the+DOM",
    },
];

const VideoGallery = () => {
  return (
    <div className="container-responsive py-8 md:py-16">
      <h1 className="text-responsive-3xl md:text-responsive-5xl font-bold text-white text-center mb-8 md:mb-12">
        Meet Our Experts
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 lg:gap-8">
        {videoData.map((video) => (
          <VideoItem key={video.id} video={video} />
        ))}
      </div>
    </div>
  );
};

const VideoItem = ({ video }) => {
  const videoRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(true); // Start as true for autoplay

  const handlePlayPause = () => {
    if (isPlaying) {
      videoRef.current.pause();
    } else {
      videoRef.current.play();
    }
    setIsPlaying(!isPlaying);
  };

  return (
    <div className="bg-gray-900 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105">
      <div className="relative aspect-video bg-black">
        <video
          className="w-full h-full object-cover"
          ref={videoRef}
          autoPlay
          muted
          loop
          playsInline
        >
          <source src={video.url} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        {/* Play button */}
        <button
          className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-30 text-white text-3xl md:text-4xl hover:bg-opacity-50 transition-all duration-300 touch-target"
          onClick={handlePlayPause}
          style={{ display: isPlaying ? "none" : "flex" }}
          aria-label="Play video"
        >
          <i className="fas fa-play"></i>
        </button>
        {/* Pause button */}
        <button
          className="absolute top-4 right-4 bg-black bg-opacity-50 text-white p-2 rounded-full hover:bg-opacity-70 transition-all duration-300 touch-target"
          onClick={handlePlayPause}
          style={{ display: isPlaying ? "block" : "none" }}
          aria-label="Pause video"
        >
          <i className="fas fa-pause"></i>
        </button>
      </div>
      <div className="p-4">
        <h2 className="text-responsive-base md:text-responsive-lg font-semibold text-white text-center">
          {video.title}
        </h2>
      </div>
    </div>
  );
};

export default VideoGallery;
