import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// import analyze from "rollup-plugin-analyzer";

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: [{ find: '@', replacement: '/src' }],
  },
  plugins: [vue()],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:5000/api",
        rewrite: (path) => path.replace(/^\/api/, ""),
        changeOrigin: true,
      },
      "/logout": {
        target: "http://localhost:5000",
        changeOrigin: true,
      }
    },
  },
  build: {
    rollupOptions: {
      // plugins: [analyze({ limit: 10 })],
    }
  }
})
