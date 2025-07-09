#!/bin/sh

# Production start script for Docker container
echo "🚀 Starting Techrypt Production Services..."

# Set production environment
export NODE_ENV=production

# Start chatbot in background
echo "🤖 Starting chatbot..."
cd /app
python3 smart_llm_chatbot.py &

# Start server
echo "📡 Starting server..."
cd /app/server
node app.js
