import React, { useRef, useState } from 'react';
import emailjs from '@emailjs/browser';
import { toast } from 'react-toastify';
import { TailSpin } from 'react-loader-spinner'; // or any other spinner you prefer

export default function ContactForm() {
    const formRef = useRef();
    const [isLoading, setIsLoading] = useState(false);

    console.log({
        serviceId: import.meta.env.VITE_EMAILJS_SERVICE_ID,
        templateId: import.meta.env.VITE_EMAILJS_TEMPLATE_ID,
        publicKey: import.meta.env.VITE_EMAILJS_PUBLIC_KEY
    });

    const sendEmail = (e) => {
        e.preventDefault();
        setIsLoading(true);

        emailjs
            .sendForm(
                import.meta.env.VITE_EMAILJS_SERVICE_ID,
                import.meta.env.VITE_EMAILJS_TEMPLATE_ID,
                formRef.current,
                import.meta.env.VITE_EMAILJS_PUBLIC_KEY,
            )
            .then(
                (result) => {
                    console.log(result.text);
                    toast.success('Message sent successfully!');
                    formRef.current.reset();
                },
                (error) => {
                    console.error(error.text);
                    toast.error('Failed to send message: ' + error.text);
                }
            )
            .finally(() => {
                setIsLoading(false);
            });
    };

    return (
        <div className="flex flex-col items-center justify-center gap-5">
            <form ref={formRef} onSubmit={sendEmail} className="w-full max-w-4xl">
                <div className="flex flex-col md:flex-row gap-5 justify-center">
                    <div className="flex flex-col gap-5 w-full md:w-72">
                        <input
                            type="text"
                            name="from_name"
                            placeholder="Your Name"
                            className="w-full bg-transparent text-white px-3 py-2 border-b-2 border-white focus:outline-none text-xl"
                            required
                            disabled={isLoading}
                        />
                        <input
                            type="email"
                            name="from_email"
                            placeholder="Your Email"
                            className="w-full bg-transparent text-white px-3 py-2 border-b-2 border-white focus:outline-none text-xl"
                            required
                            disabled={isLoading}
                        />
                    </div>
                    <div className="flex flex-col gap-5 w-full md:w-72">
                        <input
                            type="text"
                            name="company_name"
                            placeholder="Your Company name"
                            className="w-full bg-transparent text-white px-3 py-2 border-b-2 border-white focus:outline-none text-xl"
                            disabled={isLoading}
                        />
                        <div className='border-b'>
                            <select
                                name="referral_source"
                                className="w-full bg-transparent text-white px-3 border-none focus:outline-none text-xl mt-1 h-12"
                                disabled={isLoading}
                            >
                                <option value="How Did You Hear About Us?">How Did You Hear About Us?</option>
                                <option value="Social media">I found your profile on social media</option>
                                <option value="Google search">You appeared while googling</option>
                                <option value="Recommendation">Someone recommended you</option>
                                <option value="Ads">I saw your ads</option>
                                <option value="Article">Find your article or company profile</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div className="mt-5">
                    <input
                        type="text"
                        name="message"
                        placeholder="Your Goals / KPIs / Vision"
                        className="w-full bg-transparent text-white px-3 py-2 border-b-2 border-white focus:outline-none text-xl"
                        required
                        disabled={isLoading}
                    />
                </div>

                <button
                    type="submit"
                    className={`px-5 py-3 text-xl font-bold rounded-full mt-8 glow-hover bg-primary transition-all duration-150 flex items-center  text-white justify-center mx-auto gap-2 ${isLoading ? 'opacity-75 cursor-not-allowed' : ''}`}
                    disabled={isLoading}
                >
                    {isLoading ? (
                        <>
                            <TailSpin
                                height="24"
                                width="24"
                                color="#ffffff"
                                ariaLabel="loading"
                            />
                            Sending...
                        </>
                    ) : (
                        'Submit'
                    )}
                </button>
            </form>
        </div>
    );
}