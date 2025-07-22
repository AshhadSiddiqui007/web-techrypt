import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  base: '/', // ✅ THIS FIXES ASSET LOADING IN PRODUCTION
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:5000', // optional: used only in dev
    },
  },
})
