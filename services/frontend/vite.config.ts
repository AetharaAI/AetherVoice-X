import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");

  return {
    plugins: [react()],
    server: {
      port: Number(env.FRONTEND_PORT || 3000),
      proxy: {
        "/v1": env.VITE_DEV_PROXY_TARGET || `http://localhost:${env.GATEWAY_PORT || 8080}`,
        "/metrics": env.VITE_DEV_PROXY_TARGET || `http://localhost:${env.GATEWAY_PORT || 8080}`
      }
    }
  };
});
