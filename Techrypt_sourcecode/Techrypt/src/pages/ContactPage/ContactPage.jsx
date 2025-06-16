import React from 'react'
import ContactForm from '../../components/ContactForm/ContactForm'

export default function ContactPage() {
    return (
        <div className='pt-24 md:pt-40 px-4 md:px-0 min-h-screen bg-black'>
            <h1 className="text-responsive-3xl md:text-responsive-5xl text-white text-center flex justify-center items-center mb-8 md:mb-16 font-bold">
                Contact Us
            </h1>
            <div className="container-responsive">
                <ContactForm />
            </div>
        </div>
    )
}
