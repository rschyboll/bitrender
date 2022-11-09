import react from '@vitejs/plugin-react';
import { visualizer } from 'rollup-plugin-visualizer';
import { URL, fileURLToPath } from 'url';
import { defineConfig } from 'vite';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), visualizer({ template: 'sunburst' })],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          ajv: ['ajv'],
        },
      },
    },
  },
  resolve: {
    alias: {
      '@/': `${fileURLToPath(new URL('./src', import.meta.url))}/`,
    },
  },
});
