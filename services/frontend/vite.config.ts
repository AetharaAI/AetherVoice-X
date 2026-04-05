import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const allowedHosts = (env.VITE_ALLOWED_HOSTS || "")
    .split(",")
    .map((value) => value.trim())
    .filter(Boolean);
  const proxyTarget = env.VITE_DEV_PROXY_TARGET || `http://localhost:${env.GATEWAY_PORT || 8080}`;

  return {
    plugins: [react()],
    server: {
      port: Number(env.FRONTEND_PORT || 3000),
      allowedHosts: allowedHosts.length ? allowedHosts : true,
      fs: {
        deny: [
          "**/Dockerfile",
          "**/docker-compose*.yml",
          "**/package-lock.json",
          "**/tsconfig*.json",
          "**/vite.config.*",
        ],
      },
      hmr: {
        // This console is exposed on public hostnames; avoid shipping blocking
        // error overlays to operators when a non-source file is accidentally requested.
        overlay: false,
      },
      proxy: {
        "/api": proxyTarget,
        "/v1": proxyTarget,
        "/metrics": proxyTarget,
        "/ws": {
          target: proxyTarget,
          ws: true,
        },
      }
    }
  };
});
