/// <reference types="vitest" />
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { analyzer } from "vite-bundle-analyzer";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), analyzer()],
  test: {
  globals: true,
  environment: 'happy-dom',
  setupFiles: ['src/setupTest.ts']
}
})
