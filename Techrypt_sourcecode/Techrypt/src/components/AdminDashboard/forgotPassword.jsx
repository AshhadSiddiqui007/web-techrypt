// ForgotPassword.jsx
import React, { useState } from 'react';
import axios from 'axios';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    setSuccess(null);
    setLoading(true);
    try {
      await axios.post('/api/admin/forgot-password', { email });
      setSuccess('Password reset email sent!');
    } catch (error) {
      setError(error.response?.data?.message || error.message);
    }
    setLoading(false);
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#181818', // Slightly lighter than #121212 for contrast
      }}
    >
      <form
        onSubmit={handleSubmit}
        style={{
          background: '#121212',
          padding: '1.5rem 1.5rem',
          borderRadius: '8px',
          boxShadow: '0 2px 12px rgba(0,0,0,0.10)',
          minWidth: '270px',
          maxWidth: '320px',
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem',
        }}
      >
        <h3 style={{ margin: 0, textAlign: 'center', color: '#fff', fontWeight: 600, fontSize: '1.2rem' }}>
          Forgot Password
        </h3>
        <label htmlFor="email" style={{ color: '#bbb', fontSize: '0.95rem', fontWeight: 500 }}>
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
          style={{
            width: '100%',
            padding: '0.45rem 0.7rem',
            borderRadius: '5px',
            border: '1px solid #333',
            fontSize: '1rem',
            background: '#232323',
            color: '#fff',
            outline: 'none',
          }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{
            width: '100%',
            padding: '0.6rem',
            background: '#007bff',
            color: '#fff',
            border: 'none',
            borderRadius: '5px',
            fontWeight: 600,
            fontSize: '1rem',
            cursor: loading ? 'not-allowed' : 'pointer',
            marginTop: '0.5rem',
            transition: 'background 0.2s',
          }}
        >
          {loading ? 'Sending...' : 'Send Reset Email'}
        </button>
        {error && (
          <div style={{ color: '#ff4d4f', marginTop: '0.5rem', textAlign: 'center', fontSize: '0.95rem' }}>
            {error}
          </div>
        )}
        {success && (
          <div style={{ color: '#4caf50', marginTop: '0.5rem', textAlign: 'center', fontSize: '0.95rem' }}>
            {success}
          </div>
        )}
      </form>
    </div>
  );
};

export default ForgotPassword;