import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    include: [
      "@mui/material",
      "@mui/icons-material",
      "react-leaflet",
      "@react-three/fiber",
      "@react-three/drei",
      "stats.js" // UMD version of Stats.js
    ],
    exclude: [], // Nothing to exclude; Drei included now
  },
  resolve: {
    alias: {
      // Optional: ensure consistent ESM resolution if needed
      // "stats.js": "stats.js/build/stats.min.js"
    },
  },
  server: {
    fs: { strict: false },
    hmr: { timeout: 30000 }, // extend HMR timeout for large projects
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          three: ["@react-three/fiber", "@react-three/drei"],
          mui: ["@mui/material", "@mui/icons-material"],
          leaflet: ["react-leaflet"],
        },
      },
    },
  },
});
