import React from 'react'
import ContactForm from '../../components/ContactForm/ContactForm'

export default function ContactPage() {
    return (
        <div className='pt-40'>
            <h1 className="text-4xl md:text-6xl text-white text-center flex justify-center items-center mb-16">
                Contact Us
            </h1>
            <ContactForm />
        </div>
    )
}
