import React from "react";

const TermsConditions = () => {
    return (
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12 pt-4 md:pt-44">
            {/* Header */}
            <div className="text-center mb-16">
                <h1 className="text-4xl md:text-5xl font-bold text-primary mb-4">
                    Terms and Conditions
                </h1>
                <p className="text-lg text-primaryLight">
                    Last Updated: {new Date().toLocaleDateString()}
                </p>
            </div>

            {/* Content */}
            <div className="bg-six rounded-xl shadow-lg p-6 md:p-10">
                {/* Introduction */}
                <section className="mb-12">
                    <h2 className="text-2xl font-bold text-white mb-4">1. Introduction</h2>
                    <p className="text-white/70 leading-relaxed">
                        Welcome to Techrypt.io. These Terms and Conditions govern your use of our AI automation platform and services. By accessing or using our services, you agree to be bound by these terms.
                    </p>
                </section>

                {/* User Responsibilities */}
                <section className="mb-12">
                    <h2 className="text-2xl font-bold text-white mb-4">2. User Responsibilities</h2>
                    <div className="space-y-4">
                        <div className="flex items-start">
                            <div className="flex-shrink-0 h-5 w-5 text-primary mt-1 mr-2">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                </svg>
                            </div>
                            <p className="text-white/70">You must be at least 18 years old to use our services.</p>
                        </div>
                        <div className="flex items-start">
                            <div className="flex-shrink-0 h-5 w-5 text-primary mt-1 mr-2">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                </svg>
                            </div>
                            <p className="text-white/70">You are responsible for maintaining the confidentiality of your account credentials.</p>
                        </div>
                        <div className="flex items-start">
                            <div className="flex-shrink-0 h-5 w-5 text-primary mt-1 mr-2">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                </svg>
                            </div>
                            <p className="text-white/70">You agree not to use our services for any illegal or unauthorized purpose.</p>
                        </div>
                    </div>
                </section>

                {/* Intellectual Property */}
                <section className="mb-12">
                    <h2 className="text-2xl font-bold text-white mb-4">3. Intellectual Property</h2>
                    <div className="bg-six/10 rounded-lg p-6">
                        <ul className="space-y-3">
                            {[
                                "All content, features, and functionality on our platform are owned by us and protected by intellectual property laws",
                                "You may not modify, reproduce, or distribute any content without our express permission",
                                "User-generated content remains your property, but you grant us a license to use it for service operation and improvement"
                            ].map((item, index) => (
                                <li key={index} className="flex items-start">
                                    <div className="flex-shrink-0 h-5 w-5 text-primaryLight mt-0.5 mr-2">
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2h-1V9z" clipRule="evenodd" />
                                        </svg>
                                    </div>
                                    <span className="text-white/70">{item}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                </section>

                {/* Payments and Subscriptions */}
                <section className="mb-12">
                    <h2 className="text-2xl font-bold text-white mb-4">4. Payments and Subscriptions</h2>
                    <div className="grid md:grid-cols-2 gap-6">
                        {[
                            {
                                icon: (
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                                    </svg>
                                ),
                                title: "Payment Terms",
                                text: "All fees are non-refundable except as required by law"
                            },
                            {
                                icon: (
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                ),
                                title: "Subscription Renewals",
                                text: "Subscriptions automatically renew unless canceled before the renewal date"
                            }
                        ].map((item, index) => (
                            <div key={index} className="bg-six/10 p-6 rounded-lg">
                                <div className="text-primaryLight mb-3">{item.icon}</div>
                                <h3 className="text-lg font-semibold text-white mb-2">{item.title}</h3>
                                <p className="text-white/70">{item.text}</p>
                            </div>
                        ))}
                    </div>
                </section>

                {/* Limitation of Liability */}
                <section className="mb-12">
                    <h2 className="text-2xl font-bold text-white mb-4">5. Limitation of Liability</h2>
                    <p className="text-white/70 mb-4">
                        To the maximum extent permitted by law, we shall not be liable for:
                    </p>
                    <ul className="list-disc pl-6 space-y-2 text-white/70">
                        <li>Any indirect, incidental, or consequential damages</li>
                        <li>Loss of profits, data, or business opportunities</li>
                        <li>Errors or inaccuracies in our AI-generated outputs</li>
                    </ul>
                </section>

                {/* Governing Law */}
                <section className="mb-12">
                    <h2 className="text-2xl font-bold text-white mb-4">6. Governing Law</h2>
                    <p className="text-white/70 leading-relaxed">
                        These Terms shall be governed by and construed in accordance with the laws of Pakistan, without regard to its conflict of law provisions.
                    </p>
                </section>

                {/* Changes to Terms */}
                <section className="mb-12">
                    <h2 className="text-2xl font-bold text-white mb-4">7. Changes to Terms</h2>
                    <p className="text-white/70 leading-relaxed">
                        We reserve the right to modify these terms at any time. We will notify you of significant changes through our platform or via email.
                    </p>
                </section>

                {/* Contact */}
                <section className="bg-primary/10 rounded-xl p-8">
                    <h2 className="text-2xl font-bold text-white mb-4">Contact Us</h2>
                    <p className="text-white/70 mb-4">
                        For questions about these Terms and Conditions:
                    </p>
                    <div className="space-y-2">
                        <p className="flex items-center text-white">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-primaryLight" viewBox="0 0 20 20" fill="currentColor">
                                <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                                <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                            </svg>
                            Email: INFO@TECHRYPT.IO
                        </p>
                        <p className="flex items-center text-white">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-primaryLight" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                            </svg>
                            Address: Karachi, Pakistan
                        </p>
                    </div>
                </section>
            </div>
        </div>
    );
};

export default TermsConditions;