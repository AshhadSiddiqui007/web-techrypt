import { useRef, useState } from 'react';
import { toast } from 'react-toastify';
import { TailSpin } from 'react-loader-spinner';
import emailjs from '@emailjs/browser';

export default function Form() {
    const formRef = useRef()
    const [isLoading, setIsLoading] = useState(false);

    const [formData, setFormData] = useState({
        name: '',
        email: '',
        businessType: ''
    });
    const [showModal, setShowModal] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setShowModal(true);
        // Here you would typically send the data to your backend
        console.log('Form submitted:', formData);
        sendEmail(e)
    };

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
        <div className="min-h-screen bg-black flex items-center justify-center p-4">
            <form ref={formRef} onSubmit={handleSubmit} className="w-full max-w-3xl p-8">
                <h2 className="text-white text-4xl font-bold mb-5 lg:mb-7 text-center">Bussiness Form</h2>

                <div className="mb-6">
                    <label htmlFor="name" className="block text-gray-300 text-xl font-medium">
                        Name
                    </label>
                    <input
                        type="text"
                        id="name"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border-b border-white bg-transparent text-white focus:outline-none  "
                        required
                    />
                </div>

                <div className="mb-6">
                    <label htmlFor="email" className="block text-gray-300 text-xl font-medium">
                        Email
                    </label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border-b border-white bg-transparent text-white focus:outline-none  "
                        required
                    />
                </div>

                <div className="mb-6">
                    <label htmlFor="businessType" className="block text-gray-300 text-xl font-medium">
                        Business Type
                    </label>
                    <input
                        id="businessType"
                        name="businessType"
                        value={formData.businessType}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border-b border-white bg-transparent text-white focus:outline-none  "
                        required
                    >
                        {/* <option value="">Select your business type</option>
                        <option value="Retail">Retail</option>
                        <option value="Service">Service</option>
                        <option value="Manufacturing">Manufacturing</option>
                        <option value="Other">Other</option> */}
                    </input>
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

            {/* Thank You Modal */}
            {showModal && !isLoading && (
                <div className="fixed inset-0 glowing-green bg-black bg-opacity-75 flex items-center justify-center p-4 z-50">
                    <div className="bg-black rounded-lg shadow-xl max-w-md w-full p-6 relative">
                        <h3 className="text-2xl font-bold text-white mb-4">Thank You!</h3>
                        <p className="text-gray-300 mb-6">
                            Thank you for submitting your information. We'll get back to you soon.
                        </p>
                        <button
                            onClick={() => setShowModal(false)}
                            className="w-full bg-primary  text-white font-medium py-2 px-4 rounded-md transition duration-300"
                        >
                            Close
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}