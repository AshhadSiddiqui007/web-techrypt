const express = require("express")
const dotenv = require("dotenv").config()
const connectDb = require("./config/database")
const {errorHandlerMiddleWare,notFound}=require("./middlewares/errorHandler")
const cors = require("cors")
const AdminRoutes = require("./routes/AdminRoutes")
const newsletterRoutes = require('./routes/newsletterRoutes');
const appointmentRoutes = require('./routes/appointmentRoutes');
const contactRoutes = require('./routes/contactRoutes');

connectDb()

const PORT = process.env.PORT || 5000
const app=express()

app.use(cors())
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

app.get("/", (req, res) => {
    res.send("Welcome to Techrypt")
})

app.get("/api/test-new-server", (req, res) => {
    res.json({ success: true, message: "This is the NEW server!" });
});

app.use("/api/admin",AdminRoutes)
app.use('/api', newsletterRoutes);
app.use('/api', appointmentRoutes);
app.use('/api', contactRoutes);

app.use(notFound)
app.use(errorHandlerMiddleWare)

app.listen(PORT,()=>{
    console.log("Server is running on port 5000")
})

