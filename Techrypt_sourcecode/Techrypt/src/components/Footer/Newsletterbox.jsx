import React, { useState } from "react";
import './Newsletterbox.css';

const Newsletterbox = () => {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState(""); // "success", "error", or ""

  const handleSubscribe = async (e) => {
    e.preventDefault();
    setStatus("");
    try {
      const res = await fetch("http://localhost:5000/api/subscribe-newsletter", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      const data = await res.json();
      if (res.ok && data.success) {
        setStatus("success");
        setEmail("");
      } else {
        setStatus("error");
      }
    } catch (err) {
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