const express = require('express');
const router = express.Router();
const newsletterController = require('../controllers/newsletterController');
// const adminController = require('../controllers/AdminControllers');

router.post('/save-newsletter', newsletterController.saveNewsletterContent);
router.post('/send-newsletter', newsletterController.sendNewsletter);
router.get('/latest-newsletter', newsletterController.getLatestNewsletter);
// router.get('/newsletter-stats', adminController.getNewsletterStats);

module.exports = router;