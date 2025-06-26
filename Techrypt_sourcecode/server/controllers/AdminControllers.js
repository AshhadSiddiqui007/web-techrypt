const AdminModel = require("../models/AdminModel")
const generateToken = require("../utils/generateToken")
const bcrypt = require("bcrypt")
const asyncHandler = require('express-async-handler')

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


module.exports = {
    adminLogin,
    getMe,
}







