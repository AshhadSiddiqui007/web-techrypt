import React, { useState } from "react";
import { motion } from "framer-motion";
import "./Newsletterbox.css"; // Assuming you'll move the styles to a separate CSS file

export default function Newsletterbox() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState({ message: "", type: "" });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Basic email validation
    if (!email || !email.includes('@')) {
      setStatus({ message: "Please enter a valid email address", type: "error" });
      return;
    }
    
    // Set loading state
    setIsSubmitting(true);
    setStatus({ message: "Subscribing...", type: "" });
    
    try {
      // Send subscription request to server
      const response = await fetch('/api/subscribe-newsletter', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email })
      });
      
      const data = await response.json();
      
      if (data.success) {
        setStatus({ message: "Thank you for subscribing!", type: "success" });
        setEmail(""); // Clear input on success
        
        // Clear success message after 5 seconds
        setTimeout(() => {
          setStatus({ message: "", type: "" });
        }, 5000);
      } else {
        setStatus({ 
          message: data.error || "Subscription failed. Please try again.", 
          type: "error" 
        });
      }
    } catch (error) {
      console.error('Newsletter subscription error:', error);
      setStatus({ 
        message: "Something went wrong. Please try again later.", 
        type: "error" 
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <motion.div 
      className="newsletter-container"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <h4 className="newsletter-heading">Subscribe to Our Newsletter</h4>
      <form className="newsletter-form" onSubmit={handleSubmit}>
        <input 
          type="email" 
          className="newsletter-input" 
          placeholder="Enter your email" 
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <button 
          type="submit" 
          className="newsletter-button"
          disabled={isSubmitting}
        >
          {isSubmitting ? "Subscribing..." : "Subscribe Now"}
        </button>
      </form>
      {status.message && (
        <motion.div 
          className={`newsletter-status ${status.type}`}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {status.message}
        </motion.div>
      )}
    </motion.div>
  );
}