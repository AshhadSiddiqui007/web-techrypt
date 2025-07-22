import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { FiArrowLeft, FiCalendar, FiUser, FiEye, FiTag } from 'react-icons/fi';

const BlogDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [blog, setBlog] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchBlogDetail();
  }, [id]);

  const fetchBlogDetail = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${import.meta.env.VITE_NODE_BACKEND}/blogs/${id}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Blog Detail API Response:', data);
      
      if (data.success && data.data) {
        setBlog(data.data);
      } else {
        setError('Blog not found');
      }
    } catch (err) {
      console.error('Error fetching blog:', err);
      setError('Failed to load blog. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex justify-center items-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-black flex flex-col justify-center items-center text-center">
        <h1 className="text-4xl font-bold text-white mb-4">Oops!</h1>
        <p className="text-red-500 mb-6">{error}</p>
        <button
          onClick={() => navigate('/blog')}
          className="px-6 py-3 bg-primary text-black rounded-lg hover:bg-primary/90 transition-colors"
        >
          Back to Blog List
        </button>
      </div>
    );
  }

  if (!blog) {
    return (
      <div className="min-h-screen bg-black flex flex-col justify-center items-center text-center">
        <h1 className="text-4xl font-bold text-white mb-4">Blog Not Found</h1>
        <p className="text-gray-400 mb-6">The blog you're looking for doesn't exist.</p>
        <button
          onClick={() => navigate('/blog')}
          className="px-6 py-3 bg-primary text-black rounded-lg hover:bg-primary/90 transition-colors"
        >
          Back to Blog List
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header/Navigation */}
      <div className="container mx-auto px-4 py-6">
        <button
          onClick={() => navigate('/blog')}
          className="flex items-center gap-2 text-primary hover:text-primary/80 transition-colors mb-6"
        >
          <FiArrowLeft /> Back to Blog List
        </button>
      </div>

      {/* Blog Content */}
      <article className="container mx-auto px-4 pb-12">
        {/* Blog Header */}
        <header className="mb-8">
          {/* Featured Image */}
          {blog.image && (
            <div className="mb-8">
              <img
                src={`${import.meta.env.VITE_NODE_BACKEND}${blog.image}`}
                alt={blog.blog_title}
                className="w-full h-[400px] md:h-[500px] object-cover rounded-lg"
              />
            </div>
          )}

          {/* Title */}
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-6 leading-tight">
            {blog.blog_title}
          </h1>

          {/* Meta Information */}
          <div className="flex flex-wrap items-center gap-6 text-gray-400 mb-8">
            <div className="flex items-center gap-2">
              <FiUser className="text-primary" />
              <span>By {blog.author}</span>
            </div>
            <div className="flex items-center gap-2">
              <FiCalendar className="text-primary" />
              <span>{formatDate(blog.createdAt)}</span>
            </div>
            <div className="flex items-center gap-2">
              <FiEye className="text-primary" />
              <span>{blog.views} views</span>
            </div>
          </div>

          {/* Tags */}
          {blog.tags && blog.tags.length > 0 && (
            <div className="flex items-center gap-2 mb-8">
              <FiTag className="text-primary" />
              <div className="flex flex-wrap gap-2">
                {blog.tags.map((tag, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-gray-800 text-primary rounded-full text-sm"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}
        </header>

        {/* Blog Content */}
        <div className="prose prose-lg prose-invert max-w-none">
          <div className="text-gray-300 leading-relaxed whitespace-pre-line text-lg">
            {blog.content}
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 pt-8 border-t border-gray-800">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="text-gray-400">
              <p>Published on {formatDate(blog.createdAt)}</p>
              {blog.updatedAt !== blog.createdAt && (
                <p className="text-sm">Last updated on {formatDate(blog.updatedAt)}</p>
              )}
            </div>
            
            <div className="flex gap-4">
              <button
                onClick={() => navigate('/blog')}
                className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition-colors"
              >
                Back to Blog List
              </button>
              <Link
                to="/contact"
                className="px-6 py-2 bg-primary text-black rounded-lg hover:bg-primary/90 transition-colors"
              >
                Contact Us
              </Link>
            </div>
          </div>
        </footer>
      </article>
    </div>
  );
};

export default BlogDetailPage;
