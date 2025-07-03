const asyncHandler = require('express-async-handler');
const Blog = require('../models/Blog');
const fs = require('fs');
const path = require('path');

// @desc    Get all blogs with pagination
// @route   GET /api/blogs?page=1&limit=10&includeAll=true
// @access  Public (includeAll requires admin)
const getAllBlogs = asyncHandler(async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const skip = (page - 1) * limit;
    const includeAll = req.query.includeAll === 'true';

    // If includeAll is requested, get all blogs (for admin)
    // Otherwise, only get published blogs (for public)
    const filter = includeAll ? {} : { status: 'published' };

    // Get total count for pagination info
    const totalBlogs = await Blog.countDocuments(filter);
    
    // Get blogs with pagination
    const blogs = await Blog.find(filter)
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(limit);

    const totalPages = Math.ceil(totalBlogs / limit);
    const hasNextPage = page < totalPages;
    const hasPreviousPage = page > 1;

    res.json({
      success: true,
      data: blogs,
      pagination: {
        currentPage: page,
        totalPages,
        totalBlogs,
        blogsPerPage: limit,
        hasNextPage,
        hasPreviousPage
      }
    });
  } catch (error) {
    res.status(500);
    throw new Error('Server Error');
  }
});

// @desc    Get single blog
// @route   GET /api/blogs/:id
// @access  Public
const getBlogById = asyncHandler(async (req, res) => {
  try {
    const blog = await Blog.findById(req.params.id);
    
    if (!blog) {
      res.status(404);
      throw new Error('Blog not found');
    }

    // Increment views
    blog.views += 1;
    await blog.save();

    res.json({
      success: true,
      data: blog
    });
  } catch (error) {
    res.status(500);
    throw new Error('Server Error');
  }
});

// @desc    Create new blog
// @route   POST /api/blogs
// @access  Private/Admin
const createBlog = asyncHandler(async (req, res) => {
  try {
    const { blog_title, content, tags, status, author, scheduledDate } = req.body;

    if (!blog_title || !content) {
      res.status(400);
      throw new Error('Please provide blog title and content');
    }

    const blogData = {
      blog_title,
      content,
      author: author || 'Admin',
      status: status || 'published'
    };

    if (scheduledDate && status === 'scheduled') {
      blogData.scheduledDate = new Date(scheduledDate); // ✅ Correct placement
    }

    if (tags) {
      blogData.tags = Array.isArray(tags)
        ? tags
        : tags.split(',').map(tag => tag.trim());
    }

    if (req.file) {
      blogData.image = `/images/BlogsCovers/${req.file.filename}`;
    }

    const blog = await Blog.create(blogData);

    res.status(201).json({
      success: true,
      data: blog
    });
  } catch (error) {
    res.status(500);
    throw new Error('Server Error');
  }
});


// @desc    Update blog
// @route   PUT /api/blogs/:id
// @access  Private/Admin
const updateBlog = asyncHandler(async (req, res) => {
  try {
    let blog = await Blog.findById(req.params.id);

    if (!blog) {
      res.status(404);
      throw new Error('Blog not found');
    }

    const { blog_title, content, tags, status, author, scheduledDate } = req.body;

    const updateData = {
      blog_title: blog_title || blog.blog_title,
      content: content || blog.content,
      author: author || blog.author,
      status: status || blog.status,
    };

    // Handle scheduled date logic
    if (scheduledDate && status === 'scheduled') {
      updateData.scheduledDate = new Date(scheduledDate);
    } else if (status !== 'scheduled') {
      updateData.scheduledDate = null; // Reset if not scheduled anymore
    }

    if (tags) {
      updateData.tags = Array.isArray(tags)
        ? tags
        : tags.split(',').map(tag => tag.trim());
    }

    // Handle new image upload
    if (req.file) {
      // Delete old image if exists
      if (blog.image) {
        const oldImagePath = path.join(__dirname, '../../Techrypt/public', blog.image);
        if (fs.existsSync(oldImagePath)) {
          fs.unlinkSync(oldImagePath);
        }
      }
      updateData.image = `/images/BlogsCovers/${req.file.filename}`;
    }

    blog = await Blog.findByIdAndUpdate(req.params.id, updateData, {
      new: true,
      runValidators: true
    });

    res.json({
      success: true,
      data: blog
    });
  } catch (error) {
    console.error(error);
    res.status(500);
    throw new Error('Server Error');
  }
});

// @desc    Delete blog
// @route   DELETE /api/blogs/:id
// @access  Private/Admin
const deleteBlog = asyncHandler(async (req, res) => {
  try {
    const blog = await Blog.findById(req.params.id);

    if (!blog) {
      res.status(404);
      throw new Error('Blog not found');
    }

    // Delete associated image
    if (blog.image) {
      const imagePath = path.join(__dirname, '../../Techrypt/public', blog.image);
      if (fs.existsSync(imagePath)) {
        fs.unlinkSync(imagePath);
      }
    }

    await Blog.findByIdAndDelete(req.params.id);

    res.json({
      success: true,
      message: 'Blog deleted successfully'
    });
  } catch (error) {
    res.status(500);
    throw new Error('Server Error');
  }
});

// @desc    Get blogs by status
// @route   GET /api/blogs/status/:status
// @access  Public
const getBlogsByStatus = asyncHandler(async (req, res) => {
  try {
    const { status } = req.params;
    const blogs = await Blog.find({ status }).sort({ createdAt: -1 });
    
    res.json({
      success: true,
      count: blogs.length,
      data: blogs
    });
  } catch (error) {
    res.status(500);
    throw new Error('Server Error');
  }
});

module.exports = {
  getAllBlogs,
  getBlogById,
  createBlog,
  updateBlog,
  deleteBlog,
  getBlogsByStatus
};
