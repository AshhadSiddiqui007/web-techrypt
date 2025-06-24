const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');
const path = require('path');

router.post('/subscribe-newsletter', async (req, res) => {
  try {
    const { email } = req.body;
    
    // Basic validation
    if (!email || !email.includes('@')) {
      return res.status(400).json({ success: false, error: 'Invalid email address' });
    }
    
    // Create a promise to handle the Python subprocess
    const pythonResult = await new Promise((resolve, reject) => {
      const pythonProcess = spawn('python', [
        path.join(__dirname, '../python_scripts/add_subscriber.py'),
        email
      ]);
      
      let resultData = '';
      let errorData = '';
      
      pythonProcess.stdout.on('data', (data) => {
        resultData += data.toString();
      });
      
      pythonProcess.stderr.on('data', (data) => {
        errorData += data.toString();
      });
      
      pythonProcess.on('close', (code) => {
        if (code !== 0) {
          reject(new Error(errorData || 'Process exited with code ' + code));
          return;
        }
        
        try {
          resolve(JSON.parse(resultData));
        } catch (e) {
          reject(new Error('Invalid JSON response from Python script'));
        }
      });
    });
    
    return res.json(pythonResult);
    
  } catch (error) {
    console.error('Newsletter subscription error:', error);
    return res.status(500).json({
      success: false,
      error: 'Server error. Please try again later.'
    });
  }
});

module.exports = router;