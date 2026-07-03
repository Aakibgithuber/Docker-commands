# syntax=docker/dockerfile:1

# ---- Node.js production image ------------------------------------------------
# Pin a specific minor version and use the small Alpine variant.
FROM node:20-alpine

# Create app directory owned by the built-in non-root `node` user.
WORKDIR /app

# Copy manifests first so dependency install is cached separately from source.
COPY package*.json ./

# Install only production dependencies. `npm ci` when a lockfile exists is
# preferred in real projects; this sample has no runtime deps so install is a
# no-op but keeps the layer explicit.
RUN npm install --omit=dev && npm cache clean --force

# Copy the rest of the source.
COPY . .

# Drop root privileges — the official image ships a `node` user.
USER node

ENV NODE_ENV=production \
    PORT=3000

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1:3000/health || exit 1

CMD ["node", "server.js"]
