const express = require("express")
require('dotenv').config();
const axios = require('axios');
const cron = require('node-cron');
const NewsletterContent = require('./models/NewsletterContent');
const startScheduledBlogPublisher = require('./utils/schedule');

// Debug environment variables
console.log("=== ENVIRONMENT VARIABLES DEBUG ===")
console.log("NODE_ENV:", process.env.NODE_ENV)
console.log("PORT:", process.env.PORT)
console.log("JWT_SECRET:", process.env.JWT_SECRET ? "SET" : "UNDEFINED")
console.log("JWT_SECRET value:", process.env.JWT_SECRET)
console.log("MONGODB_URI:", process.env.MONGODB_URI ? "SET" : "UNDEFINED")
console.log("=====================================")

const connectDb = require("./config/database")
const {errorHandlerMiddleWare,notFound}=require("./middlewares/errorHandler")
const cors = require("cors")
const path = require("path")
const AdminRoutes = require("./routes/AdminRoutes")
const newsletterRoutes = require('./routes/newsletterRoutes');
const appointmentRoutes = require('./routes/appointmentRoutes');
const contactRoutes = require('./routes/contactRoutes');
const blogRoutes = require('./routes/blogRoutes');

connectDb()

const PORT = process.env.PORT || 5000
const app=express()

app.use(cors())
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

// Serve static files for blog images
app.use('/images', express.static(path.join(__dirname, '../Techrypt/public/images')))

app.get("/", (req, res) => {
    res.send("Welcome to Techrypt")
})

app.get("/api/test", (req, res) => {
    res.json({ message: "API is working", timestamp: new Date().toISOString() });
});

app.use("/api/admin", AdminRoutes);
app.use('/api', newsletterRoutes);
app.use('/api', appointmentRoutes);
app.use('/api', contactRoutes);
app.use('/api/blogs', blogRoutes);

console.log('Newsletter routes mounted at /api');
console.log('Available endpoints:');
console.log('POST /api/subscribe');
console.log('POST /api/contact-info');
console.log('POST /api/save-newsletter');
console.log('POST /api/send-newsletter');
console.log('GET /api/latest-newsletter');

// Schedule to run at 9:00 AM on the 1st of every month
cron.schedule('0 9 1 * *', async () => {
    const latest = await NewsletterContent.findOne().sort({ createdAt: -1 });
    if (!latest) return;
    await axios.post('http://localhost:5000/api/send-newsletter', {
        subject: latest.subject,
        content: latest.content
    });
});
startScheduledBlogPublisher();

app.use(notFound)
app.use(errorHandlerMiddleWare)

app.listen(PORT,()=>{
    console.log("Server is running on port 5000")
})

