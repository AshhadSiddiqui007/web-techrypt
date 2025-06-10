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
    <>
      <h1 className="video-h1">Meet Our Experts</h1>
      <div className="video-gallery">
        {videoData.map((video) => (
          <VideoItem key={video.id} video={video} />
        ))}
      </div>
    </>
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
    <div className="video-item">
      <div className="video-container">
        <video
          className="video"
          ref={videoRef}
          autoPlay
          muted // Muted to allow autoplay in most browsers
          loop // Optional: makes the video loop
        >
          <source src={video.url} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        {/* Play button */}
        <button
          className="play-button"
          onClick={handlePlayPause}
          style={{ display: isPlaying ? "none" : "block" }}
        >
          <i className="fas fa-play"></i> {/* Font Awesome play icon */}
        </button>
        {/* Pause button */}
        <button
          className="pause-button"
          onClick={handlePlayPause}
          style={{ display: isPlaying ? "block" : "none" }}
        >
          <i className="fas fa-pause"></i> {/* Font Awesome pause icon */}
        </button>
      </div>
      <h2 className="video-h2">{video.title}</h2>
    </div>
  );
};

export default VideoGallery;
