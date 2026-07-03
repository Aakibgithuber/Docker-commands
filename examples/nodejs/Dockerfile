# syntax=docker/dockerfile:1

# ---- Stage 1: install production dependencies ----
FROM node:20-alpine AS deps
WORKDIR /app

# Copy only manifests first so dependency install is cached
# independently of application source changes.
COPY package*.json ./
# Install prod deps; ensure node_modules exists even with zero dependencies
# so the runtime COPY below always has a directory to copy.
RUN (npm ci --omit=dev || npm install --omit=dev) && mkdir -p node_modules

# ---- Stage 2: runtime ----
FROM node:20-alpine AS runtime
ENV NODE_ENV=production
WORKDIR /app

# Run as the built-in non-root "node" user for a smaller attack surface.
COPY --from=deps /app/node_modules ./node_modules
COPY --chown=node:node . .
USER node

EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD node -e "require('http').get('http://127.0.0.1:3000/health',r=>process.exit(r.statusCode===200?0:1)).on('error',()=>process.exit(1))"

CMD ["node", "app.js"]
