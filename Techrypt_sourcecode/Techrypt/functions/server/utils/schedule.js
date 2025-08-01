const cron = require('node-cron');
const Blog = require('../models/Blog'); // adjust path if your structure differs

// Function to start cron job
const startScheduledBlogPublisher = () => {
  console.log('⏰ Blog scheduler initialized to run every 10 minutes...');

  // Cron: Run every 10 minutes
  cron.schedule('*/10 * * * *', async () => {
    try {
      const now = new Date();

      // Find blogs scheduled to be published at or before current time
      const scheduledBlogs = await Blog.find({
        status: 'scheduled',
        scheduledDate: { $lte: now }
      });

      for (const blog of scheduledBlogs) {
        blog.status = 'published';
        blog.scheduledDate = null;
        await blog.save();
        console.log(`✅ Scheduled blog published: ${blog.blog_title}`);
      }

      if (scheduledBlogs.length === 0) {
        console.log('ℹ️ No blogs to publish this minute.');
      }
    } catch (error) {
      console.error('❌ Error publishing scheduled blogs:', error);
    }
  });
};

module.exports = startScheduledBlogPublisher;
