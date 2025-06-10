import React from "react";
import Cards from "../../components/Cards/Card";
import Hero from "../../components/Hero/Hero";
import Filter from "../../components/Filter/Filter";
import Form from "./Form/Form";

const Offers = () => {
    return (
        <>
            <div style={{ backgroundColor: "#0f0f0f" }}>
                <Hero still={true} title={["Get Your Business AI-Ready in 30 Days"]} text={
                    <div className="flex flex-col items-center gap-2">We Build Your Website, Automate Bookings, & Grow Sales Using AI-Driven Systems.
                        <button className="bg-primary hover:bg-primaryLight cursor-pointer text-white py-3 px-4 rounded-full">Free Strategy Call or Download Free AI Blueprint.
                        </button>
                    </div>} />
                <div className="fading"></div>
                <Form />

            </div>
        </>
    );
};

export default Offers;
