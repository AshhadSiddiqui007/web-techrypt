const express = require('express');
const router = express.Router();
const newsletterController = require('../controllers/newsletterController');

router.post('/save-newsletter', newsletterController.saveNewsletterContent);
router.post('/send-newsletter', newsletterController.sendNewsletter);
router.get('/latest-newsletter', newsletterController.getLatestNewsletter);
router.get('/newsletter-stats', newsletterController.getNewsletterStats);
router.post('/subscribe', newsletterController.subscribe);

module.exports = router;