import React from "react";

const PrivacyPolicy = () => {
    return (
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12 pt-10 md:pt-44">
            {/* Header */}
            <div className="text-center mb-16">
                <h1 className="text-4xl md:text-5xl font-bold text-primary mb-4">
                    Privacy Policy
                </h1>
                <p className="text-lg text-primaryLight">
                    Last Updated: {new Date().toLocaleDateString()}
                </p>
            </div>

            {/* Policy Content */}
            <div className="bg-six rounded-xl shadow-lg p-6 md:p-10">
                {/* Introduction */}
                <section className="mb-12">
                    <h2 className="text-2xl font-bold text-white mb-4">1. Introduction</h2>
                    <p className="text-white/70 leading-relaxed">
                        Techrypt.io,
                        an AI automation platform that provides AI-driven workflow automation tools.
                        We are committed to protecting your privacy. This policy explains how we collect,
                        use, disclose, and safeguard your information when you use our services.
                    </p>
                </section>

                {/* Information We Collect */}
                <section className="mb-12">
                    <h2 className="text-2xl font-bold text-white mb-4">2. Information We Collect</h2>

                    <div className="mb-6">
                        <h3 className="text-xl font-semibold text-white/90 mb-2">A. Personal Data</h3>
                        <p className="text-white/70 mb-4">
                            We may collect:
                        </p>
                        <ul className="list-disc pl-6 space-y-2 text-white/70">
                            <li><span className="font-medium text-primaryLight">Contact Information:</span> Name, email, phone number, job title.</li>
                            <li><span className="font-medium text-primaryLight">Account Details:</span> Username, password, payment information.</li>
                            <li><span className="font-medium text-primaryLight">User Content:</span> Files or data you upload to our AI systems.</li>
                            <li><span className="font-medium text-primaryLight">Communications:</span> Emails, chat logs, or support tickets.</li>
                        </ul>
                    </div>

                    <div>
                        <h3 className="text-xl font-semibold text-white/90 mb-2">B. Automated Data Collection</h3>
                        <ul className="list-disc pl-6 space-y-2 text-white/70">
                            <li><span className="font-medium text-primaryLight">Usage Data:</span> IP address, browser type, device information.</li>
                            <li><span className="font-medium text-primaryLight">Cookies & Tracking:</span> We use cookies to improve user experience.</li>
                            <li><span className="font-medium text-primaryLight">AI Training Data:</span> Anonymous data to improve our algorithms.</li>
                        </ul>
                    </div>
                </section>

                {/* How We Use Your Information */}
                <section className="mb-12">
                    <h2 className="text-2xl font-bold text-white mb-4">3. How We Use Your Information</h2>
                    <div className="grid md:grid-cols-2 gap-4">
                        {[
                            "Provide, operate, and maintain our AI services",
                            "Improve algorithms and develop new features",
                            "Process transactions and send service notices",
                            "Respond to inquiries and offer support",
                            "Send promotional emails (opt-out available)",
                            "Comply with legal obligations"
                        ].map((item, index) => (
                            <div key={index} className="flex items-start">
                                <div className="flex-shrink-0 h-5 w-5 text-primary mt-1 mr-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                    </svg>
                                </div>
                                <p className="text-white/70">{item}</p>
                            </div>
                        ))}
                    </div>
                </section>

                {/* Data Sharing */}
                <section className="mb-12">
                    <h2 className="text-2xl font-bold text-white mb-4">4. Data Sharing & Disclosure</h2>
                    <p className="text-white/70 mb-4">
                        We <span className="font-bold text-primaryLight">do not sell</span> your personal data. Limited sharing occurs with:
                    </p>
                    <div className="bg-six/10 rounded-lg p-6">
                        <ul className="space-y-3">
                            {[
                                "Service Providers: Payment processors, cloud hosting (e.g., AWS)",
                                "Legal Compliance: If required by law (e.g., subpoenas)",
                                "Business Transfers: In case of mergers/acquisitions"
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

                {/* Data Security */}
                <section className="mb-12">
                    <h2 className="text-2xl font-bold text-white mb-4">5. Data Security</h2>
                    <div className="grid md:grid-cols-3 gap-6">
                        {[
                            {
                                icon: (
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                    </svg>
                                ),
                                title: "Encryption",
                                text: "SSL/TLS for data in transit; AES-256 for data at rest"
                            },
                            {
                                icon: (
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                                    </svg>
                                ),
                                title: "Access Controls",
                                text: "Strict employee access limitations"
                            },
                            {
                                icon: (
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                                    </svg>
                                ),
                                title: "AI Protections",
                                text: "Input data is anonymized for model training"
                            }
                        ].map((item, index) => (
                            <div key={index} className="bg-six/10 p-6 rounded-lg">
                                <div className="text-primaryLight mb-3">{item.icon}</div>
                                <h3 className="text-lg font-semibold text-white mb-2">{item.title}</h3>
                                <p className="text-white/70">{item.text}</p>
                            </div>
                        ))}
                    </div>
                    <p className="mt-4 text-sm italic text-white/50">
                        Note: No system is 100% secure. You acknowledge this risk by using our services.
                    </p>
                </section>

                {/* Contact */}
                <section className="bg-primary/10 rounded-xl p-8">
                    <h2 className="text-2xl font-bold text-white mb-4">Contact Us</h2>
                    <p className="text-white/70 mb-4">
                        For questions or requests regarding your privacy:
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

export default PrivacyPolicy;