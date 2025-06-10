import React, { useState } from 'react';
import { FaLinkedin, FaYoutube, FaFacebookSquare, FaTwitter } from 'react-icons/fa';
import { RiArrowUpDoubleLine, RiInstagramFill } from 'react-icons/ri';
import { motion } from 'framer-motion';
import { clutch, google, meta, techryptLogo } from '../../assets/mainImages';
import ContactForm from '../ContactForm/ContactForm';
import TopModal from '../TopModal/TopModal';
import PrivacyPolicy from '../PrivacyPolicy/PrivacyPolicy';
import { Link, useLocation } from 'react-router-dom';


const Footer = () => {
  const location = useLocation()
  const [privacy, setPrivacy] = useState(false);
  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  };


  return (
    <div className="text-center bg-[#000] mt-10 overflow-x-hidden pt-24 px-3">
      <div className="inline-flex flex-col items-center justify-center mb-12">
        <img className="mx-auto object-contain w-72 mb-2" src={techryptLogo} alt="Techrypt Logo" />
        <h3 className="text-lg font-bold text-white mt-2 px-5 py-2 border-2 border-white rounded-full inline-block">
          Empowering Digital Skills & AI-Driven Business Solutions
        </h3>
        <div className="w-full h-24 pt-8 flex justify-center">
          <motion.div
            className="bg-white w-0.5"
            initial={{ height: 0 }}
            whileInView={{ height: '100px' }}
            viewport={{ once: false }}
            transition={{ duration: 0.8, ease: 'easeOut', delay: 0.3 }}
          />
        </div>
      </div>

      {location.pathname !== "/Contact" && <ContactForm />}
      <div className="relative top-5 flex flex-col text-gray-400 mb-12 leading-8">
        <span>
          By clicking submit, you agree to our{' '}
          <Link to={"/PrivacyPolicy"} className=" text-primary">
            Privacy Policy
          </Link>
        </span>
        <span>
          {' '} and{' '}
          <Link to={"Terms&Conditions"} className="text-primary">
            Terms and Conditions
          </Link>
        </span>
      </div>

      <div className="flex gap-4 md:gap-10 lg:gap-20 justify-center items-center">
        <a href="/">
          <FaLinkedin className="text-4xl text-white glowing-green transition-all duration-150" />
        </a>
        <a href="/">
          <FaYoutube className="text-4xl text-white glowing-green transition-all duration-150" />
        </a>
        <a href="/">
          <RiInstagramFill className="text-4xl text-white glowing-green transition-all duration-150" />
        </a>
        <a href="/">
          <FaFacebookSquare className="text-4xl text-white glowing-green transition-all duration-150" />
        </a>
        <a href="/">
          <FaTwitter className="text-4xl text-white glowing-green transition-all duration-150" />
        </a>
      </div>



      <div className="flex md:px-10 py-10 px-2 max-md:flex-col items-center md:items-end justify-between gap-5 w-full mb-12">

        <div className="  flex flex-col items-center justify-start  gap-5 max-md:order-3 max-md:mt-7">
          <div
            className="h-10 md:w-16 w-10 md:h-16    flex justify-center items-center  text-5xl text-primary cursor-pointer rounded-full border border-primary hover:bg-primary hover:text-white glowing-yellow transition-all duration-300  "
            title='Scroll to top'
            onClick={scrollToTop}
          // style={{ 
          //   backgroundImage:
          //     `url("data:image/svg+xml;charset=utf-8;base64,PHN2ZyB3aWR0aD0iOTYiIGhlaWdodD0iOTYiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iNDgiIGN5PSI0OCIgcj0iNDciIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIyIi8+PHBhdGggZD0iTTIzIDE3aDUwIiBzdHJva2U9IiNmZmYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PHBhdGggZD0iTTQ3IDgxYTEgMSAwIDEgMCAyIDBoLTJabTItNTZhMSAxIDAgMSAwLTIgMGgyWk0yOS41NjggNDEuNDhhMSAxIDAgMSAwIDAgMnYtMlpNNDkuMDQ4IDI0YTEgMSAwIDEgMC0yIDBoMlptMTcuMSAxOS4xYTEgMSAwIDEgMCAwLTJ2MlpNNDkgODFWMjVoLTJ2NTZoMlpNMjkuNTY4IDQzLjQ4YzQuNzk1IDAgOC40NTgtMS4yMDEgMTEuMjM4LTMuMDU1IDIuNzc1LTEuODUgNC42MTItNC4zMDkgNS44MjctNi43MzggMS4yMTItMi40MjQgMS44MTMtNC44MzcgMi4xMTMtNi42MzUuMTUtLjkwMS4yMjYtMS42NTUuMjY0LTIuMTg3YTE2LjU3IDE2LjU3IDAgMCAwIC4wMzgtLjg0NFYyNC4wMDFsLTEtLjAwMWgtMXYtLjAwMS4wMzdsLS4wMDQuMTM4Yy0uMDA0LjEyNC0uMDEyLjMxLS4wMy41NDktLjAzNC40NzktLjEwMiAxLjE2OS0uMjQxIDItLjI3OCAxLjY2Ny0uODMyIDMuODc1LTEuOTMgNi4wNy0xLjA5NSAyLjE5MS0yLjcyMyA0LjM1Mi01LjE0NiA1Ljk2OC0yLjQxNyAxLjYxLTUuNjg0IDIuNzItMTAuMTMgMi43MnYyWk00OC4wNDggMjRsLTEgLjAwMXYuMDA2YS43NTQuNzU0IDAgMCAwIDAgLjA2MWwuMDA1LjE2OWMuMDA1LjE0NC4wMTQuMzUxLjAzMy42MTIuMDM3LjUyMS4xMTEgMS4yNi4yNTkgMi4xNDQuMjkzIDEuNzYyLjg4MyA0LjEyNyAyLjA3MSA2LjUwNCAxLjE5IDIuMzgyIDIuOTkyIDQuNzkzIDUuNzE0IDYuNjA3IDIuNzI3IDEuODE4IDYuMzE4IDIuOTk2IDExLjAxOCAyLjk5NnYtMmMtNC4zNSAwLTcuNTQ2LTEuMDg0LTkuOTEtMi42Ni0yLjM2OS0xLjU4LTMuOTYtMy42OTMtNS4wMzMtNS44MzctMS4wNzQtMi4xNDgtMS42MTYtNC4zMDgtMS44ODgtNS45NGEyMS4yMTggMjEuMjE4IDAgMCAxLS4yMzYtMS45NTcgMTQuMjQgMTQuMjQgMCAwIDEtLjAzMi0uNjd2LS4wMzdsLTEgLjAwMVoiIGZpbGw9IiNmZmYiLz48L3N2Zz4=")`
          // }}
          >
            <RiArrowUpDoubleLine />
          </div>
          <a href="mailto:INFO@TECHRYPT.IO" className="text-gray-400 text-xs glowing-green">
            INFO@TECHRYPT.IO
          </a>
        </div>
        <div className=" flex gap-10 justify-center    text-gray-400">
         
          <Link to={"/PrivacyPolicy"} onClick={() => setPrivacy(true)} className="">
            Privacy Policy
          </Link>
          <Link to={"/Terms&Conditions"} className="ml-1">
            Terms & Conditions
          </Link>
        </div>

      </div>
      {/* <TopModal isOpen={privacy} onClose={() => setPrivacy(false)}>
        <PrivacyPolicy />
      </TopModal> */}
    </div>
  );
};

export default Footer;