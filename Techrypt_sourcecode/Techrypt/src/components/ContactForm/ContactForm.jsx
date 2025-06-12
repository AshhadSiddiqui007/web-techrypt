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
    <div className="bg-[#1a1a1a] border border-gray-800 rounded-lg p-6 w-full max-w-md mx-auto">
      <h3 className="text-xl font-bold text-white mb-4">Contact Us</h3>
      
      <form onSubmit={handleSubmit}>
        <div className="space-y-4">
          <div>
            <label className="block text-gray-300 mb-1">Full Name *</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className="w-full bg-[#2a2a2a] border border-gray-700 rounded-lg px-4 py-2 text-white"
              placeholder="John Doe"
            />
          </div>
          
          <div>
            <label className="block text-gray-300 mb-1">Email Address *</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full bg-[#2a2a2a] border border-gray-700 rounded-lg px-4 py-2 text-white"
              placeholder="john@example.com"
            />
          </div>
          
          <div>
            <label className="block text-gray-300 mb-1">Phone Number</label>
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              className="w-full bg-[#2a2a2a] border border-gray-700 rounded-lg px-4 py-2 text-white"
              placeholder="e.g., 1234567890"
            />
          </div>
          
          <div>
            <label className="block text-gray-300 mb-1">Message</label>
            <textarea
              name="message"
              value={formData.message}
              onChange={handleChange}
              rows="4"
              className="w-full bg-[#2a2a2a] border border-gray-700 rounded-lg px-4 py-2 text-white"
              placeholder="How can we help you?"
            ></textarea>
          </div>
        </div>
        
        <button
          type="submit"
          className="mt-6 w-full bg-primary text-white rounded-lg py-3 font-medium hover:bg-primary/90"
        >
          Send Message
        </button>
      </form>
    </div>
  );
};

export default ContactForm;
