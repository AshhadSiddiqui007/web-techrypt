import React from "react";
import SectionComponent from "./Section";
import { creative1, creative2, rocket, target } from "../../assets/mainImages";
import ParallaxWrapper from "../ParallaxWrapper/ParallaxWrapper";

const CreativeTeamSection = () => {
  return (
    <>
      <SectionComponent
        heading="Creative & Digital Design"
        text="From logo creation to motion graphics, social reels to post-production, we create designs that not only look good — they perform.  Key focus on  Strategy, creativity, visual storytelling, audience engagement, and brand alignment."
        imagePath={
          // "https://cdn.prod.website-files.com/65f9d9d22fb2f3b3f17c09ed/663280ce947a093198288960_home-page-inpage-1.png"
          // creative1
          rocket
        }
        bgImageSrc={"https://jam3-media.imgix.net/uploads/2023/03/101_A-1.jpg?fit=max&amp;auto=compress,format"}
        imageAlt="Storytelling Illustration"
        reverse={true}
      />
      <SectionComponent
        heading="Development, AI & Marketing Solutions"
        text="We build smart tools for smarter businesses. Whether it's custom websites, mobile apps, or AI-powered bots, we develop with purpose and scale with precision. Our marketing services — including SEO, social ads, and full-scale platform management — drive visibility and conversion."
        imagePath={
          // "https://cdn.prod.website-files.com/65f9d9d22fb2f3b3f17c09ed/663280cd47a47296bb847efc_home-page-inpage-1-1.png"
          target
        }
        bgImageSrc={"https://jam3-media.imgix.net/uploads/2020/09/CASE-STUDY-RAW-ASSETS.01_43_05_29.Still052-2.jpg?fit=max&auto=compress,format&w=1440&dpr=1"}
        imageAlt="Creative Mind"
      />
      {/* <SectionComponent
        heading="Development, AI & Marketing Solutions"
        text="We build smart tools for smarter businesses. Whether it's custom websites, mobile apps, or AI-powered bots, we develop with purpose and scale with precision. Our marketing services — including SEO, social ads, and full-scale platform management — drive visibility and conversion."
        imagePath={
          // "https://cdn.prod.website-files.com/65f9d9d22fb2f3b3f17c09ed/663280cd47a47296bb847efc_home-page-inpage-1-1.png"
          target
        }
        bgImageSrc={"https://jam3-media.imgix.net/uploads/2023/03/101_A-1.jpg?fit=max&amp;auto=compress,format"}
        imageAlt="Creative Mind"
      />
      <SectionComponent
        heading="Development, AI & Marketing Solutions"
        text="We build smart tools for smarter businesses. Whether it's custom websites, mobile apps, or AI-powered bots, we develop with purpose and scale with precision. Our marketing services — including SEO, social ads, and full-scale platform management — drive visibility and conversion."
        imagePath={
          // "https://cdn.prod.website-files.com/65f9d9d22fb2f3b3f17c09ed/663280cd47a47296bb847efc_home-page-inpage-1-1.png"
          target
        }
        bgImageSrc={"https://jam3-media.imgix.net/uploads/2020/09/CASE-STUDY-RAW-ASSETS.01_43_05_29.Still052-2.jpg?fit=max&auto=compress,format&w=1440&dpr=1"}
        imageAlt="Creative Mind"
      /> */}

    </>
  );
};

export default CreativeTeamSection;
