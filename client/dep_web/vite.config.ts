import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs';
import path from 'path';

const flagPath = path.resolve(__dirname, 'flag');
const isLocal = fs.existsSync(flagPath)
if (isLocal) {
  var domain: string = 'http://localhost:5000';
  fs.rmSync(flagPath);
} else {
  var domain: string = 'https://dep-g2ag.onrender.com/';
}

export default defineConfig({
  plugins: [react()],
  define: {
    __API_DOMAIN__: JSON.stringify(domain)
  }
})
