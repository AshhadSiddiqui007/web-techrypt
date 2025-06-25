import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

// Blog Card Component to display individual blogs
const BlogCard = ({ blog }) => {
  // Extract first 30 words for the excerpt
  const createExcerpt = (content) => {
    const words = content.split(' ');
    if (words.length <= 30) return content;
    return words.slice(0, 30).join(' ') + '...';
  };

  return (
    <div className="flex flex-col md:flex-row gap-4 mb-8 bg-[#1a1a1a] p-4 rounded-lg hover:bg-[#252525] transition-colors duration-300">
      <div className="md:w-1/3">
        <img 
          src={blog.imageUrl || 'https://placehold.co/600x400/1a1a1a/cccccc?text=Techrypt+Blog'} 
          alt={blog.title} 
          className="w-full h-[200px] object-cover rounded-md"
        />
      </div>
      <div className="md:w-2/3 flex flex-col justify-between">
        <div>
          <h3 className="text-xl md:text-2xl font-bold mb-2 text-white">{blog.title}</h3>
          <p className="text-gray-300 mb-4">{createExcerpt(blog.content)}</p>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-primary text-sm">{new Date(blog.publishedDate).toLocaleDateString()}</span>
          <Link to={`/blog/${blog.id}`} className="px-4 py-2 bg-primary text-white rounded-md hover:bg-opacity-80 transition-all">
            Read More
          </Link>
        </div>
      </div>
    </div>
  );
};

const Blog_List_View = () => {
  const [blogs, setBlogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBlogs = async () => {
      try {
        setLoading(true);
        // Replace with your actual API endpoint
        const response = await fetch('YOUR_API_ENDPOINT/blogs');
        
        // Check if the response is ok (status in the range 200-299)
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        setBlogs(data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching blogs:', err);
        setError('Failed to load blogs. Please try again later.');
        setLoading(false);
      }
    };

    fetchBlogs();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center min-h-[200px] flex items-center justify-center">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {blogs.length === 0 ? (
        <div className="text-center text-gray-400">No blogs found</div>
      ) : (
        <div className="space-y-8">
          {blogs.map((blog) => (
            <BlogCard key={blog.id} blog={blog} />
          ))}
        </div>
      )}
    </div>
  );
};

export default Blog_List_View;