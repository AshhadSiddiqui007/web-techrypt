const AdminModel = require("../models/AdminModel")
const generateToken = require("../utils/generateToken")
const bcrypt = require("bcrypt")
const asyncHandler = require('express-async-handler')
const crypto = require('crypto');
const nodemailer = require('nodemailer');
const NewsletterSubscriber = require('../models/Newsletter');

// POST /api/admin/login

const adminLogin = asyncHandler(async (req,res)=>{

    const {email,password}=req.body

    const admin = await AdminModel.findOne({email})

    if (!admin) {
    res.status(401).json({ message: "Admin not found" });
    throw new Error("Admin not Found")
   }

   const isPasswordMatch = await bcrypt.compare(password,admin.password)

   if(!isPasswordMatch){
    res.status(401).json({ message: "Invalid password" });
    throw new Error("Invalid Password")
   }else{
    res.status(200).json({
        _id: admin._id,
        email: admin.email,
        isAdmin: admin.isAdmin,
        token: generateToken(admin._id)
    })
   }
})

// GET /api/admin/me
const getMe = asyncHandler(async (req,res)=>{

    const admin = await AdminModel.findById(req.admin._id).select("-password")

    if (!admin) {
        res.status(404).json({ message: "Admin not found" });
        throw new Error("Admin not Found")
    }

    res.status(200).json(admin)

})

// POST /api/admin/forgot-password
const forgotPassword = asyncHandler(async (req, res) => {
    const { email } = req.body;
    const admin = await AdminModel.findOne({ email });
    if (!admin) {
        return res.status(404).json({ message: 'Admin not found' });
    }

    const token = crypto.randomBytes(32).toString('hex');
    admin.resetPasswordToken = token;
    admin.resetPasswordExpires = Date.now() + 3600000; // 1 hour
    await admin.save();

    // Configure your transporter for Hostinger SMTP
    const transporter = nodemailer.createTransport({
        host: 'smtp.hostinger.com',
        port: 465,
        secure: true, // true for port 465 (SSL)
        auth: {
            user: process.env.EMAIL_USER,
            pass: process.env.EMAIL_PASS,
        },
    });

    const resetUrl = `http://localhost:5173/admin/reset-password/${token}`;
    await transporter.sendMail({
        to: admin.email,
        subject: 'Password Reset',
        text: `Reset your password: ${resetUrl}`,
    });

    res.json({ message: 'Password reset link sent' });
});

// POST /api/admin/reset-password/:token
const resetPassword = asyncHandler(async (req, res) => {
    const { token } = req.params;
    const { password } = req.body;
    const admin = await AdminModel.findOne({
        resetPasswordToken: token,
        resetPasswordExpires: { $gt: Date.now() }
    });
    if (!admin) {
        return res.status(400).json({ message: 'Invalid or expired token' });
    }

    admin.password = await bcrypt.hash(password, 10);
    admin.resetPasswordToken = undefined;
    admin.resetPasswordExpires = undefined;
    await admin.save();

    res.json({ message: 'Password updated' });
});

// GET /api/admin/stats
const getAdminStats = asyncHandler(async (req, res) => {
    // TODO: Replace with real visitor count logic if you have it
    const visitorCount = 0; // Placeholder

    const newsletterCount = await NewsletterSubscriber.countDocuments();

    res.json({
        visitorCount,
        newsletterCount,
    });
});

exports.getNewsletterStats = async (req, res) => {
    try {
        // Replace this with your real visitor tracking logic if you have it
        const visitorCount = 0; // Placeholder, update if you track visitors

        const newsletterCount = await NewsletterSubscriber.countDocuments();

        res.json({
            visitorCount,
            newsletterCount,
        });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
};

module.exports = {
    adminLogin,
    getMe,
    forgotPassword,
    resetPassword,
    getAdminStats,
}







