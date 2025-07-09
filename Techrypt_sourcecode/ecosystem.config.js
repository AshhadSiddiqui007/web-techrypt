module.exports = {
  apps: [
    {
      name: 'techrypt-server',
      script: './server/app.js',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'development',
        PORT: 5000
      },
      env_production: {
        NODE_ENV: 'production',
        PORT: 5000
      },
      error_file: './logs/server-error.log',
      out_file: './logs/server-out.log',
      log_file: './logs/server-combined.log',
      time: true
    },
    {
      name: 'techrypt-chatbot',
      script: './smart_llm_chatbot.py',
      interpreter: 'python3',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '512M',
      env: {
        NODE_ENV: 'development'
      },
      env_production: {
        NODE_ENV: 'production'
      },
      error_file: './logs/chatbot-error.log',
      out_file: './logs/chatbot-out.log',
      log_file: './logs/chatbot-combined.log',
      time: true
    }
  ]
};
