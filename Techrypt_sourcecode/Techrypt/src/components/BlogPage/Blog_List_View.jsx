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
          src={blog.image ? `http://localhost:5000${blog.image}` : 'https://placehold.co/600x400/1a1a1a/cccccc?text=Techrypt+Blog'} 
          alt={blog.blog_title} 
          className="w-full h-[200px] object-cover rounded-md"
        />
      </div>
      <div className="md:w-2/3 flex flex-col justify-between">
        <div>
          <h3 className="text-xl md:text-2xl font-bold mb-2 text-white">{blog.blog_title}</h3>
          <p className="text-gray-300 mb-4">{createExcerpt(blog.content)}</p>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-primary text-sm">By {blog.author} • {new Date(blog.createdAt).toLocaleDateString()}</span>
          <Link to={`/blog/${blog._id}`} className="px-4 py-2 bg-primary text-white rounded-md hover:bg-opacity-80 transition-all">
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
  const [pagination, setPagination] = useState({
    currentPage: 1,
    totalPages: 1,
    totalBlogs: 0,
    hasNextPage: false,
    hasPreviousPage: false
  });

  // Fetch blogs with pagination
  const fetchBlogs = async (page = 1) => {
    try {
      setLoading(true);
      setError(null);
      
      // Add pagination parameters to the API call
      const response = await fetch(`http://localhost:5000/api/blogs?page=${page}&limit=10`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('API Response:', data); // Debug log
      
      if (data.success && data.data) {
        setBlogs(data.data);
        if (data.pagination) {
          setPagination(data.pagination);
        }
      } else {
        console.error('Unexpected API response structure:', data);
        setBlogs([]);
      }
      setLoading(false);
    } catch (err) {
      console.error('Error fetching blogs:', err);
      setError('Failed to load blogs. Please try again later.');
      setBlogs([]);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBlogs(1); // Start with page 1
  }, []);

  // Handle page navigation
  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= pagination.totalPages) {
      fetchBlogs(newPage);
      // Scroll to top of blog section
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

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
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-white mb-4">Our Blog</h1>
        <p className="text-gray-400 max-w-2xl mx-auto">
          Discover insights, tips, and stories from our team
        </p>
      </div>

      {blogs.length === 0 ? (
        <div className="text-center text-gray-400">No blogs found</div>
      ) : (
        <>
          {/* Blog List */}
          <div className="space-y-8 mb-12">
            {Array.isArray(blogs) && blogs.map((blog) => (
              <BlogCard key={blog._id} blog={blog} />
            ))}
          </div>

          {/* Pagination */}
          {pagination.totalPages > 1 && (
            <div className="flex justify-center items-center space-x-4">
              {/* Previous Button */}
              <button
                onClick={() => handlePageChange(pagination.currentPage - 1)}
                disabled={!pagination.hasPreviousPage}
                className={`px-6 py-2 rounded-lg font-medium transition-colors ${
                  pagination.hasPreviousPage
                    ? "bg-primary text-black hover:bg-primary/90"
                    : "bg-gray-600 text-gray-400 cursor-not-allowed"
                }`}
              >
                Previous
              </button>

              {/* Page Numbers */}
              <div className="flex items-center space-x-2">
                {Array.from({ length: pagination.totalPages }, (_, i) => i + 1).map((pageNum) => {
                  // Show current page and adjacent pages
                  if (
                    pageNum === pagination.currentPage ||
                    pageNum === pagination.currentPage - 1 ||
                    pageNum === pagination.currentPage + 1 ||
                    pageNum === 1 ||
                    pageNum === pagination.totalPages
                  ) {
                    return (
                      <button
                        key={pageNum}
                        onClick={() => handlePageChange(pageNum)}
                        className={`w-10 h-10 rounded-lg font-medium transition-colors ${
                          pageNum === pagination.currentPage
                            ? "bg-primary text-black"
                            : "bg-gray-700 text-white hover:bg-gray-600"
                        }`}
                      >
                        {pageNum}
                      </button>
                    );
                  } else if (
                    pageNum === pagination.currentPage - 2 ||
                    pageNum === pagination.currentPage + 2
                  ) {
                    return <span key={pageNum} className="text-gray-400">...</span>;
                  }
                  return null;
                })}
              </div>

              {/* Next Button */}
              <button
                onClick={() => handlePageChange(pagination.currentPage + 1)}
                disabled={!pagination.hasNextPage}
                className={`px-6 py-2 rounded-lg font-medium transition-colors ${
                  pagination.hasNextPage
                    ? "bg-primary text-black hover:bg-primary/90"
                    : "bg-gray-600 text-gray-400 cursor-not-allowed"
                }`}
              >
                Next
              </button>
            </div>
          )}

          {/* Blog Stats */}
          <div className="text-center mt-8 text-gray-400">
            Showing {blogs.length} of {pagination.totalBlogs} blogs
          </div>
        </>
      )}
    </div>
  );
};

export default Blog_List_View;