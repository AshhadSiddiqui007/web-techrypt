const jwt = require("jsonwebtoken")

const generateToken = (id) => {
  console.log("=== generateToken DEBUG ===")
  console.log("User ID:", id)
  console.log("JWT_SECRET:", process.env.JWT_SECRET ? "SET" : "UNDEFINED")
  console.log("JWT_SECRET value:", process.env.JWT_SECRET)
  console.log("========================")
  
  if (!process.env.JWT_SECRET) {
    throw new Error("JWT_SECRET environment variable is not set")
  }
  
  return jwt.sign({ id }, process.env.JWT_SECRET, {
    expiresIn: "1d",
  });
};

module.exports = generateToken
// This function generates a JWT token using the provided user ID and a secret key from environment variables.
// The token is set to expire in 1 day.