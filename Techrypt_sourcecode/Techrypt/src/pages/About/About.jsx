import React from 'react'
import AboutPara from '../../components/AboutPara/AboutPara'
import AboutWrite from '../../components/AboutWrite/AboutWrite'
import AboutSlider from '../../components/AboutSlider/AboutSlider'
import Hero from '../../components/Hero/Hero'
import AboutAwards from '../../components/AboutAwards/AboutAwards'
import Plans from '../../components/Plans/Plans'
import AboutCards from '../../components/AboutCards/AboutCards'
import OurVision from '../../components/OurVision/OurVision'
import ParallaxWrapper from '../../components/ParallaxWrapper/ParallaxWrapper'


const About = () => {
  return (
    <>
      <div style={{
        backgroundColor: "#0f0f0f",
      }}>
        <Hero text={" Unlock new opportunities with expert-led training & cutting-edge digital services.Techrypt.io is a forward-thinking team on a mission to revolutionize how individuals learn and how businesses grow."} />
        <div className="fading"></div>

        <AboutPara />

        {/* Move Plans (packages) section higher for better visibility */}
        <Plans />

        <AboutSlider />
        <ParallaxWrapper
          children={[
            <AboutCards />,
            <OurVision />
          ]}
        />
        <ParallaxWrapper
          children={[
            <AboutWrite />
          ]}
        />
        {/* <AboutAwards/> */}
      </div>
    </>
  )
}

export default About