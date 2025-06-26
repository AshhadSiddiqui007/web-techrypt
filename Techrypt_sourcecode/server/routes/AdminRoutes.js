const express = require("express")
const {adminLogin,getMe}= require("../controllers/AdminControllers")
const {protectAdmin}= require("../middlewares/authMiddleWare")

const router = express.Router()

// POST /api/admin/login
router.post("/login", adminLogin)
// GET /api/admin/me
router.get("/me", protectAdmin, getMe)

module.exports = router