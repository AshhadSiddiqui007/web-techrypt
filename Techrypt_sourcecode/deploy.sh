#!/bin/bash

# Production Deployment Script for Techrypt
echo "🚀 Starting Techrypt Production Deployment..."

# Set production environment
export NODE_ENV=production

# Navigate to project directory
cd /path/to/your/server/directory

# Install dependencies
echo "📦 Installing server dependencies..."
npm install --production

# Start server with PM2 (process manager)
echo "🔄 Starting server with PM2..."
pm2 start ecosystem.config.js --env production

# Navigate to frontend directory
cd ../Techrypt

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install

# Build frontend for production
echo "🏗️ Building frontend for production..."
npm run build:prod

# Copy built files to web server directory
echo "📁 Copying built files to web server..."
cp -r dist/* /var/www/html/

# Start chatbot
echo "🤖 Starting chatbot..."
cd ..
python3 smart_llm_chatbot.py &

echo "✅ Deployment completed successfully!"
echo "🌐 Your website should be live at your domain"
echo "📡 API Server: Running on port 5000"
echo "🤖 Chatbot: Running on port 5001"
