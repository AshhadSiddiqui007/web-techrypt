import React from 'react';
import '../../pages/LandingPages/PRLandingPage.css';

const TalkingBubble = () => {
  return (
    <section className="pr-landing-section text-center mx-auto pt-0.5 pb-1">
      <div className="pr-talking-anim">
        <div className="pr-talking-person">
          <span className="pr-talking-bubble">Let's connect!</span>
        </div>
        <div className="pr-talking-person green">
          <span className="pr-talking-bubble">Excited to share news!</span>
        </div>
        <div className="pr-talking-person">
          <span className="pr-talking-bubble">Ready for your story?</span>
        </div>
      </div>
    </section>
  );
};

export default TalkingBubble;