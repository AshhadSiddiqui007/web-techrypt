import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AdminSidebar from './AdminSidebar';

const AdminNewsletterUpload = () => {
  const [subject, setSubject] = useState('');
  const [content, setContent] = useState('');
  const [msg, setMsg] = useState('');
  const [loading, setLoading] = useState(false);
  const [latest, setLatest] = useState(null);
  const [stats, setStats] = useState({ visitorCount: 0, newsletterCount: 0 });

  useEffect(() => {
    axios.get('/api/latest-newsletter')
      .then(res => setLatest(res.data))
      .catch(() => setLatest(null));
    axios.get('/api/newsletter-stats')
      .then(res => setStats(res.data))
      .catch(() => setStats({ visitorCount: 0, newsletterCount: 0 }));
  }, [msg]); // refetch after save

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg('');
    setLoading(true);
    try {
      await axios.post('/api/save-newsletter', { subject, content });
      setMsg('Newsletter saved for next send!');
      setSubject('');
      setContent('');
    } catch (err) {
      setMsg('Error: ' + (err.response?.data?.error || err.message));
    }
    setLoading(false);
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: '#181818' }}>
      <div style={{ minWidth: 220, background: '#121212' }}>
        <AdminSidebar currentSection="newsletter" />
      </div>
      <div style={{ flex: 1, padding: '2rem', color: '#fff' }}>
        <h2 style={{ textAlign: 'center', marginBottom: 20 }}>Upload Newsletter</h2>
        {/* Stats Section */}
        <div style={{ display: 'flex', gap: 24, marginBottom: 24 }}>
          <div style={{ background: '#232323', padding: 16, borderRadius: 8, minWidth: 160 }}>
            <div style={{ fontSize: 14, color: '#bbb' }}>Visitors</div>
            <div style={{ fontSize: 22, fontWeight: 600 }}>{stats.visitorCount}</div>
          </div>
          <div style={{ background: '#232323', padding: 16, borderRadius: 8, minWidth: 160 }}>
            <div style={{ fontSize: 14, color: '#bbb' }}>Newsletter Subscribers</div>
            <div style={{ fontSize: 22, fontWeight: 600 }}>{stats.newsletterCount}</div>
          </div>
        </div>
        {latest && (
          <div style={{
            background: '#232323',
            color: '#fff',
            padding: 16,
            borderRadius: 8,
            marginBottom: 24
          }}>
            <h4 style={{ margin: 0 }}>Latest Newsletter</h4>
            <div><b>Subject:</b> {latest.subject}</div>
            <div><b>Content:</b> <div dangerouslySetInnerHTML={{ __html: latest.content }} /></div>
            <div style={{ fontSize: '0.85rem', color: '#bbb', marginTop: 8 }}>
              Last updated: {new Date(latest.createdAt).toLocaleString()}
            </div>
          </div>
        )}
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 16, maxWidth: 420, margin: '0 auto' }}>
          <label>
            Subject:
            <input
              type="text"
              value={subject}
              onChange={e => setSubject(e.target.value)}
              required
              style={{
                width: '100%',
                padding: '0.5rem',
                marginTop: 4,
                borderRadius: 4,
                border: '1px solid #333',
                background: '#232323',
                color: '#fff'
              }}
            />
          </label>
          <label>
            Content (HTML allowed):
            <textarea
              value={content}
              onChange={e => setContent(e.target.value)}
              required
              rows={8}
              style={{
                width: '100%',
                padding: '0.5rem',
                marginTop: 4,
                borderRadius: 4,
                border: '1px solid #333',
                background: '#232323',
                color: '#fff',
                resize: 'vertical'
              }}
            />
          </label>
          <button
            type="submit"
            disabled={loading}
            style={{
              background: '#007bff',
              color: '#fff',
              border: 'none',
              borderRadius: 4,
              padding: '0.7rem',
              fontWeight: 600,
              fontSize: '1rem',
              cursor: loading ? 'not-allowed' : 'pointer'
            }}
          >
            {loading ? 'Saving...' : 'Save Newsletter'}
          </button>
          {msg && <div style={{ marginTop: 10, textAlign: 'center', color: msg.startsWith('Error') ? '#ff4d4f' : '#4caf50' }}>{msg}</div>}
        </form>
      </div>
    </div>
  );
};

export default AdminNewsletterUpload;