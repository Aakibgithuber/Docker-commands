# syntax=docker/dockerfile:1

# ---- Production Node.js image ----
# Pin a specific minor version and use the small Alpine variant.
FROM node:20-alpine

# Create and use a dedicated app directory.
WORKDIR /app

# Copy manifests first so `npm install` is cached unless dependencies change.
COPY package*.json ./
RUN npm install --omit=dev && npm cache clean --force

# Copy the rest of the application source.
COPY . .

# Run as the built-in non-root `node` user instead of root.
USER node

ENV NODE_ENV=production \
    PORT=3000
EXPOSE 3000

# Lightweight healthcheck hitting the /health endpoint.
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', r => process.exit(r.statusCode === 200 ? 0 : 1)).on('error', () => process.exit(1))"

CMD ["node", "server.js"]
