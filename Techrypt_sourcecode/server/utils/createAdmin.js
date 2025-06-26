const mongoose = require("mongoose");
const dotenv = require("dotenv").config();
const Admin = require("../models/AdminModel");
const bcrypt = require("bcrypt");
const asyncHandler = require("express-async-handler");

const createAdmin = asyncHandler(async () => {
  const adminEmail = process.env.ADMIN_EMAIL;
  const adminPassword = process.env.ADMIN_PASSWORD;

  if (!adminEmail || !adminPassword) {
    console.error("Admin email or password not provided in environment variables");
    return;
  }

  // Connect to MongoDB before any query
  await mongoose.connect(process.env.MONGO_URI);

  const existingAdmin = await Admin.findOne({ email: adminEmail });
  if (existingAdmin) {
    console.log("Admin already exists");
    return;
  }

  const hashedPassword = await bcrypt.hash(adminPassword, 10);
  const newAdmin = new Admin({
    email: adminEmail,
    password: hashedPassword,
    isAdmin: true,
  });
  await newAdmin.save();
  console.log("Admin created successfully");

  // Close connection after done
  await mongoose.disconnect();
});

createAdmin().catch(err => {
  console.error("Error creating admin:", err);
  process.exit(1);
});
