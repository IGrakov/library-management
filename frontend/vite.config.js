import vue from "@vitejs/plugin-vue";
import path from "path";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    host: "0.0.0.0", // allow Docker access
    port: 5173,
    proxy: {
      // Proxy API requests to Django backend
      "/api": {
        target: "http://backend:8000", // service name in docker-compose
        changeOrigin: true,
        secure: false,
      },
    },
  },
  optimizeDeps: {
    exclude: ["@tanstack/vue-query", "vue-demi"],
  },
});
