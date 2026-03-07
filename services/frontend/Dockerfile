FROM node:22-alpine

WORKDIR /app/services/frontend

COPY services/frontend/package.json ./package.json
COPY services/frontend/tsconfig.json ./tsconfig.json
COPY services/frontend/vite.config.ts ./vite.config.ts

RUN npm install

COPY services/frontend /app/services/frontend

EXPOSE 3000

CMD ["sh", "-lc", "npm run dev -- --host 0.0.0.0 --port ${FRONTEND_PORT:-3000}"]
