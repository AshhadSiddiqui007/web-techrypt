const mongoose = require("mongoose")

const AdminSchema = new mongoose.Schema({
    email:{
        type: String,
        required: true,
        unique: true,
    },
    passowrd:{
        type: String,
        required: true,
    },
    isAdmin: {
        type: Boolean,
        default: true,
    },
},
 { timestamps: true }
)

module.exports = mongoose.model("Admin",AdminSchema)