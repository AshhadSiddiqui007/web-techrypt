const express = require("express");
const { adminLogin, getMe, forgotPassword, resetPassword, getAdminStats } = require("../controllers/AdminControllers");
const { protectAdmin } = require("../middlewares/authMiddleWare");

const router = express.Router();

// POST /api/admin/login
router.post("/login", adminLogin);

// GET /api/admin/me
router.get("/me", protectAdmin, getMe);

// POST /api/admin/forgot-password
router.post("/forgot-password", forgotPassword);

// POST /api/admin/reset-password/:token
router.post("/reset-password/:token", resetPassword);

// GET /api/admin/stats
router.get("/stats", protectAdmin, getAdminStats);

module.exports = router;