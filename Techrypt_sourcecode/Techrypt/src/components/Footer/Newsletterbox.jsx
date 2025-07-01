import React, { useState } from "react";

const Newsletterbox = () => {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState(""); // "success", "error", or ""

  const handleSubscribe = async (e) => {
    e.preventDefault();
    setStatus("");
    try {
      const res = await fetch("http://localhost:5000/api/subscribe", {
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
    <form onSubmit={handleSubscribe} className="flex flex-col md:flex-row gap-2 mt-2">
      <input
        type="email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="Subscribe to our newsletter"
        className="px-3 py-2 rounded bg-[#181818] text-white border border-gray-600 focus:border-primary"
        required
      />
      <button
        type="submit"
        className="bg-primary text-black px-4 py-2 rounded font-bold hover:bg-primary/90 transition"
      >
        Subscribe
      </button>
      {status === "success" && (
        <span className="text-green-400 ml-2">Subscribed!</span>
      )}
      {status === "error" && (
        <span className="text-red-400 ml-2">Something went wrong. Please try again later.</span>
      )}
    </form>
  );
};

export default Newsletterbox;