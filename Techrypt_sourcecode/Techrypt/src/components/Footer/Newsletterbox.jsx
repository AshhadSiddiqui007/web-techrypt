import React, { useState } from "react";
import './Newsletterbox.css';

const Newsletterbox = () => {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState(""); // "success", "error", or ""

  const handleSubscribe = async (e) => {
    e.preventDefault();
    setStatus("");
    
    if (!email || !email.includes('@')) {
      setStatus("error");
      return;
    }
    
    console.log('Attempting to subscribe with email:', email);
    
    try {
      const url = "/api/subscribe";
      const requestBody = { email };
      
      console.log('Making request to:', url);
      console.log('Request body:', requestBody);
      
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });
      
      console.log('Response status:', res.status);
      console.log('Response headers:', res.headers);
      
      const data = await res.json();
      console.log('Newsletter subscription response:', data);
      
      if (res.ok && data.success) {
        setStatus("success");
        setEmail("");
      } else {
        console.error('Newsletter subscription failed:', data.error);
        setStatus("error");
      }
    } catch (err) {
      console.error('Newsletter subscription error:', err);
      setStatus("error");
    }
  };

  return (
    <form onSubmit={handleSubscribe} className="newsletter-form newsletter-container">
      <input
        type="email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="Subscribe to our newsletter"
        className="newsletter-input"
        required
      />
      <button
        type="submit"
        className="newsletter-button"
      >
        Subscribe
      </button>
      {status === "success" && (
        <span className="newsletter-status success">Subscribed!</span>
      )}
      {status === "error" && (
        <span className="newsletter-status error">Something went wrong. Please try again later.</span>
      )}
    </form>
  );
};

export default Newsletterbox;