import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // ou host: '0.0.0.0'
    port: 3000 // ou outra porta de sua preferência
  }
})
