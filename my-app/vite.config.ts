import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
    server: {
      proxy: {
        // string shorthand: http://localhost:3000/api -> http://localhost:8080/api
        '/api': 'http://localhost:8080',
      },
    },
  //base: "front",
  plugins: [react()],
})
