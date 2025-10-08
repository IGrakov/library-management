import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', // allow Docker access
    port: 5173,
    proxy: {
      // Proxy API requests to Django backend
      '/api': {
        target: 'http://backend:8000', // service name in docker-compose
        changeOrigin: true,
        secure: false,
      },
    },
  },
  optimizeDeps: {
    exclude: ['@tanstack/vue-query', 'vue-demi'],
  },
})