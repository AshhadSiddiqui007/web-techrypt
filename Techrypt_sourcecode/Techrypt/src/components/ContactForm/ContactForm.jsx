import React, { useState } from "react";

const ContactForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: ''
  });
  
  const [formState, setFormState] = useState({
    isLoading: false,
    isSuccess: false,
    error: null
  });

  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }
    
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }
    
    if (formData.phone && !/^\+?[\d\s\-\(\)]+$/.test(formData.phone)) {
      newErrors.phone = 'Please enter a valid phone number';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setFormState({ isLoading: true, isSuccess: false, error: null });

    try {
      const response = await fetch('/api/contact-info', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();

      if (result.success) {
        setFormState({ isLoading: false, isSuccess: true, error: null });
        setFormData({ name: '', email: '', phone: '', message: '' });
      } else {
        throw new Error(result.error || 'Failed to submit form');
      }
    } catch (error) {
      setFormState({ 
        isLoading: false, 
        isSuccess: false, 
        error: error.message || 'Failed to submit form. Please try again.' 
      });
    }
  };

  return (
    <div className="bg-[#1a1a1a] rounded-lg p-6 md:p-8 w-full max-w-6xl mx-auto">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12">
        {/* Left Column - Contact Info */}
        <div className="space-y-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white">
            Get In Touch
          </h2>
          
          {/* Email Section */}
          <div className="flex items-center space-x-4">
            <div className="flex-shrink-0">
              <svg 
                className="w-8 h-8 text-[#c4d322]" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" 
                />
              </svg>
            </div>
            <div>
              <p className="text-gray-300 text-sm mb-1">Email Us:</p>
              <a 
                href="mailto:info@techrypt.io"
                className="text-[#c4d322] text-lg font-semibold hover:text-white transition-colors duration-300"
              >
                info@techrypt.io
              </a>
            </div>
          </div>

          {/* Social Links Section */}
          <div>
            <p className="text-gray-300 text-sm mb-4">Follow Us:</p>
            <div className="flex space-x-4">
              {/* LinkedIn */}
              <a 
                href="https://www.linkedin.com/company/techrypt-io/posts/?feedView=all" 
                className="w-12 h-12 bg-[#2a2a2a] rounded-lg flex items-center justify-center hover:bg-[#c4d322] transition-all duration-300 group"
              >
                <svg 
                  className="w-6 h-6 text-[#c4d322] group-hover:text-black transition-colors duration-300" 
                  fill="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </a>

              {/* Instagram */}
              <a 
                href="https://www.instagram.com/tech.rypt" 
                className="w-12 h-12 bg-[#2a2a2a] rounded-lg flex items-center justify-center hover:bg-[#c4d322] transition-all duration-300 group"
              >
                <svg 
                  className="w-6 h-6 text-[#c4d322] group-hover:text-black transition-colors duration-300" 
                  fill="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                </svg>
              </a>

              {/* Facebook */}
              <a 
                href="https://www.facebook.com/people/Techrypt/61575440404641/#" 
                className="w-12 h-12 bg-[#2a2a2a] rounded-lg flex items-center justify-center hover:bg-[#c4d322] transition-all duration-300 group"
              >
                <svg 
                  className="w-6 h-6 text-[#c4d322] group-hover:text-black transition-colors duration-300" 
                  fill="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
              </a>
            </div>
          </div>
        </div>

        {/* Right Column - Form */}
        <div>
          {formState.isSuccess && (
            <div className="mb-6 p-4 bg-[#c4d322]/10 border border-[#c4d322] rounded-lg">
              <p className="text-[#c4d322] font-medium">
                ✓ Thank you for your message! We'll get back to you soon.
              </p>
            </div>
          )}

          {formState.error && (
            <div className="mb-6 p-4 bg-red-900/20 border border-red-500 rounded-lg">
              <p className="text-red-400 font-medium">
                ✗ {formState.error}
              </p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Name Field */}
            <div>
              <label className="block text-gray-300 mb-2 text-sm font-medium">
                Full Name *
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                className={`w-full bg-[#2a2a2a] border rounded-lg px-4 py-3 text-white text-base focus:outline-none focus:ring-2 transition-all duration-300 ${
                  errors.name 
                    ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' 
                    : 'border-gray-700 focus:border-[#c4d322] focus:ring-[#c4d322]/20'
                }`}
                placeholder="John Doe"
                autoComplete="name"
              />
              {errors.name && (
                <p className="mt-1 text-red-400 text-sm">{errors.name}</p>
              )}
            </div>

            {/* Email Field */}
            <div>
              <label className="block text-gray-300 mb-2 text-sm font-medium">
                Email Address *
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className={`w-full bg-[#2a2a2a] border rounded-lg px-4 py-3 text-white text-base focus:outline-none focus:ring-2 transition-all duration-300 ${
                  errors.email 
                    ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' 
                    : 'border-gray-700 focus:border-[#c4d322] focus:ring-[#c4d322]/20'
                }`}
                placeholder="john@example.com"
                autoComplete="email"
                inputMode="email"
              />
              {errors.email && (
                <p className="mt-1 text-red-400 text-sm">{errors.email}</p>
              )}
            </div>

            {/* Phone Field */}
            <div>
              <label className="block text-gray-300 mb-2 text-sm font-medium">
                Phone Number
              </label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                className={`w-full bg-[#2a2a2a] border rounded-lg px-4 py-3 text-white text-base focus:outline-none focus:ring-2 transition-all duration-300 ${
                  errors.phone 
                    ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' 
                    : 'border-gray-700 focus:border-[#c4d322] focus:ring-[#c4d322]/20'
                }`}
                placeholder="e.g., +1 (555) 123-4567"
                autoComplete="tel"
                inputMode="tel"
              />
              {errors.phone && (
                <p className="mt-1 text-red-400 text-sm">{errors.phone}</p>
              )}
            </div>

            {/* Message Field */}
            <div>
              <label className="block text-gray-300 mb-2 text-sm font-medium">
                Message
              </label>
              <textarea
                name="message"
                value={formData.message}
                onChange={handleChange}
                rows="4"
                className="w-full bg-[#2a2a2a] border border-gray-700 rounded-lg px-4 py-3 text-white text-base focus:outline-none focus:border-[#c4d322] focus:ring-2 focus:ring-[#c4d322]/20 transition-all duration-300 resize-none"
                placeholder="How can we help you?"
              ></textarea>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={formState.isLoading}
              className={`w-full rounded-lg py-4 font-semibold text-lg transition-all duration-300 transform hover:scale-105 ${
                formState.isLoading
                  ? 'bg-gray-600 text-gray-300 cursor-not-allowed'
                  : 'bg-[#c4d322] text-black hover:bg-[#c4d322]/90 shadow-lg hover:shadow-xl'
              }`}
            >
              {formState.isLoading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-gray-300" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Sending...
                </span>
              ) : (
                'Send Message'
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ContactForm;
