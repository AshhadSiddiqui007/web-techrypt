const express = require('express');
const router = express.Router();
const newsletterController = require('../controllers/newsletterController');

router.post('/save-newsletter', newsletterController.saveNewsletterContent);
router.post('/send-newsletter', newsletterController.sendNewsletter);
router.get('/latest-newsletter', newsletterController.getLatestNewsletter);
const adminController = require('../controllers/AdminControllers');
router.get('/newsletter-stats', newsletterController.getNewsletterStats);
module.exports = router;