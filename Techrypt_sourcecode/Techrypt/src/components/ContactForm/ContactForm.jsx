import React, { useState } from "react";
// Remove duplicate imports of components that should only be in main.jsx
// Keep only form-related imports

const ContactForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Form submission logic
    console.log("Form submitted:", formData);
    
    // Trigger chatbot with form data
    const event = new CustomEvent('openTechryptChatbot', {
      detail: {
        contextMessage: `Hi ${formData.name}! Thanks for reaching out. How can I help you today?`,
        businessType: 'Contact Form Submission'
      }
    });
    window.dispatchEvent(event);
  };

  return (
    <div className="bg-[#1a1a1a] border border-gray-800 rounded-lg p-4 md:p-6 w-full max-w-lg mx-auto">
      <h3 className="text-responsive-xl md:text-responsive-2xl font-bold text-white mb-4 md:mb-6 text-center">Contact Us</h3>

      <form onSubmit={handleSubmit}>
        <div className="space-y-4 md:space-y-6">
          <div>
            <label className="block text-gray-300 mb-2 text-sm md:text-base font-medium">Full Name *</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className="w-full bg-[#2a2a2a] border border-gray-700 rounded-lg px-4 py-3 md:py-4 text-white text-base focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all duration-300"
              placeholder="John Doe"
              autoComplete="name"
            />
          </div>

          <div>
            <label className="block text-gray-300 mb-2 text-sm md:text-base font-medium">Email Address *</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full bg-[#2a2a2a] border border-gray-700 rounded-lg px-4 py-3 md:py-4 text-white text-base focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all duration-300"
              placeholder="john@example.com"
              autoComplete="email"
              inputMode="email"
            />
          </div>

          <div>
            <label className="block text-gray-300 mb-2 text-sm md:text-base font-medium">Phone Number</label>
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              className="w-full bg-[#2a2a2a] border border-gray-700 rounded-lg px-4 py-3 md:py-4 text-white text-base focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all duration-300"
              placeholder="e.g., 1234567890"
              autoComplete="tel"
              inputMode="tel"
            />
          </div>

          <div>
            <label className="block text-gray-300 mb-2 text-sm md:text-base font-medium">Message</label>
            <textarea
              name="message"
              value={formData.message}
              onChange={handleChange}
              rows="4"
              className="w-full bg-[#2a2a2a] border border-gray-700 rounded-lg px-4 py-3 md:py-4 text-white text-base focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all duration-300 resize-none"
              placeholder="How can we help you?"
            ></textarea>
          </div>
        </div>

        <button
          type="submit"
          className="mt-6 md:mt-8 w-full bg-primary text-black rounded-lg py-3 md:py-4 font-semibold hover:bg-primary/90 transition-all duration-300 transform hover:scale-105 touch-target text-base md:text-lg shadow-lg hover:shadow-xl"
        >
          Send Message
        </button>
      </form>
    </div>
  );
};

export default ContactForm;
