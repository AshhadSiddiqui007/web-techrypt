# Multi-stage Dockerfile for Techrypt
FROM node:18-alpine as frontend-builder

# Build frontend
WORKDIR /app/frontend
COPY Techrypt/package*.json ./
RUN npm install
COPY Techrypt/ ./
RUN npm run build:prod

# Backend stage
FROM node:18-alpine as backend

# Install Python for chatbot
RUN apk add --no-cache python3 py3-pip

# Create app directory
WORKDIR /app

# Copy server files
COPY server/package*.json ./server/
WORKDIR /app/server
RUN npm install --production

# Copy server source
COPY server/ ./

# Copy chatbot files
WORKDIR /app
COPY smart_llm_chatbot.py ./
COPY requirements.txt ./
COPY data.csv ./

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Copy frontend build
COPY --from=frontend-builder /app/frontend/dist ./public

# Create logs directory
RUN mkdir -p /app/logs

# Expose ports
EXPOSE 5000 5001

# Start script
COPY start-production.sh ./
RUN chmod +x start-production.sh

CMD ["./start-production.sh"]
