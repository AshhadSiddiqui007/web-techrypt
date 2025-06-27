const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const {
  getAllBlogs,
  getBlogById,
  createBlog,
  updateBlog,
  deleteBlog,
  getBlogsByStatus
} = require('../controllers/blogController');
const { protectAdmin } = require('../middlewares/authMiddleWare');

const router = express.Router();

// Ensure upload directory exists
const uploadDir = path.join(__dirname, '../../Techrypt/public/images/BlogsCovers');
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
}

// Configure multer for image uploads
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, uploadDir);
  },
  filename: function (req, file, cb) {
    // Generate unique filename
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, 'blog-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const fileFilter = (req, file, cb) => {
  // Check file type
  if (file.mimetype.startsWith('image/')) {
    cb(null, true);
  } else {
    cb(new Error('Not an image! Please upload only images.'), false);
  }
};

const upload = multer({
  storage: storage,
  fileFilter: fileFilter,
  limits: {
    fileSize: 5 * 1024 * 1024 // 5MB limit
  }
});

// Public routes
router.get('/', getAllBlogs);
router.get('/status/:status', getBlogsByStatus);
router.get('/:id', getBlogById);

// Protected routes (Admin only)
router.post('/', protectAdmin, upload.single('image'), createBlog);
router.put('/:id', protectAdmin, upload.single('image'), updateBlog);
router.delete('/:id', protectAdmin, deleteBlog);

module.exports = router;
