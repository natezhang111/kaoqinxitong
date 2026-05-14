import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
<<<<<<< HEAD
    host: "127.0.0.1",
=======
    host: "0.0.0.0",
>>>>>>> 98bf8e49 (update)
    port: 5173,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
<<<<<<< HEAD
=======
      "/uploads": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
      "/faces": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
>>>>>>> 98bf8e49 (update)
    },
  },
});
