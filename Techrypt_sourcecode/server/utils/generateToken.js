const jwt = require("jsonwebtoken")

const generateToken = (id) => {
  return jwt.sign({ id }, process.env.JWT_SECRET, {
    expiresIn: "1d",
  });
};

module.exports = generateToken
// This function generates a JWT token using the provided user ID and a secret key from environment variables.
// The token is set to expire in 1 day.