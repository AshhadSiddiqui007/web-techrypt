const express = require("express")
const dotenv = require("dotenv").config()
const connectDb = require("./config/db")
const {errorHandlerMiddleWare,notFound}=require("./middlewares/errorHandler")
const cors = require("cors")
const AdminRoutes = require("./routes/AdminRoutes")

connectDb()

const PORT = process.env.PORT || 5000
const app=express()

app.use(cors())
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

app.get("/", (req, res) => {
    res.send("Welcome to Techrypt")
})


app.use("/api/admin",AdminRoutes)

app.use(notFound)
app.use(errorHandlerMiddleWare)

app.listen(PORT,()=>{
    console.log("Server is running on port 5000")
})

