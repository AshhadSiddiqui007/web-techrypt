const express = require("express")
// Load environment variables based on NODE_ENV
const envFile = process.env.NODE_ENV === 'production' ? '../.env.production' : '../.env';
require('dotenv').config({ path: envFile });
const axios = require('axios');
const cron = require('node-cron');
const NewsletterContent = require('./models/NewsletterContent');
const startScheduledBlogPublisher = require('./utils/schedule');

// Only show debug info in development
if (process.env.NODE_ENV !== 'production') {
    console.log("=== ENVIRONMENT VARIABLES DEBUG ===")
    console.log("NODE_ENV:", process.env.NODE_ENV)
    console.log("PORT:", process.env.PORT)
    console.log("JWT_SECRET:", process.env.JWT_SECRET ? "SET" : "UNDEFINED")
    console.log("MONGODB_URI:", process.env.MONGODB_URI ? "SET" : "UNDEFINED")
    console.log("SENDER_EMAIL:", process.env.SENDER_EMAIL ? "SET" : "UNDEFINED")
    console.log("SMTP_SERVER:", process.env.SMTP_SERVER)
    console.log("SMTP_PORT:", process.env.SMTP_PORT)
    console.log("=====================================")
}

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

// Production CORS configuration
const corsOptions = {
    origin: process.env.NODE_ENV === 'production' 
        ? process.env.ALLOWED_ORIGINS?.split(',') || ['https://your-domain.com']
        : ['http://localhost:3000', 'http://localhost:5173'],
    credentials: true,
    optionsSuccessStatus: 200
};

app.use(cors(corsOptions))
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

// Security middleware for production
if (process.env.NODE_ENV === 'production') {
    // Trust proxy for correct IP addresses
    app.set('trust proxy', 1);
    
    // Security headers
    app.use((req, res, next) => {
        res.setHeader('X-Content-Type-Options', 'nosniff');
        res.setHeader('X-Frame-Options', 'DENY');
        res.setHeader('X-XSS-Protection', '1; mode=block');
        res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
        res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
        next();
    });
    
    // Rate limiting
    const rateLimit = require('express-rate-limit');
    const limiter = rateLimit({
        windowMs: 15 * 60 * 1000, // 15 minutes
        max: 100 // limit each IP to 100 requests per windowMs
    });
    app.use('/api/', limiter);
}

// Serve static files for blog images
app.use('/images', express.static(path.join(__dirname, '../Techrypt/public/images')))

app.get("/", (req, res) => {
    res.send("Welcome to Techrypt")
})

app.use("/api/admin", AdminRoutes);
app.use('/api', newsletterRoutes);
app.use('/api', appointmentRoutes);
app.use('/api', contactRoutes);
app.use('/api/blogs', blogRoutes);

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

