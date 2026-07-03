# Docker Commands, Documentation & Examples

Production-grade Docker reference and runnable example images. This repository
collects the Docker commands you use day to day, the best practices that matter
in real systems and interviews, and minimal-but-correct example Dockerfiles for
five popular runtimes.

## Contents

- **[`docs/docker-commands.md`](docs/docker-commands.md)** — command reference
  for `build`, `run`, `exec`, `logs`, volumes and networking, with explanations
  and the flags that matter.
- **[`docs/best-practices.md`](docs/best-practices.md)** — interview-level and
  real-world production best practices, plus a deployment checklist.
- **[`examples/`](examples/)** — small, self-contained apps with
  production-style Dockerfiles for **Node.js, Python, Java, Go and PHP**.
- **[`docker commands.txt`](docker%20commands.txt)** — the original quick command
  cheatsheet.

## Example images

Each example is a tiny HTTP service that responds on `/` and `/health`. They are
dependency-light so they build offline and quickly, while still demonstrating
production practices: pinned/minimal base images, multi-stage builds where
compilation applies, non-root users, `HEALTHCHECK`s and graceful shutdown.

| Language | Base image | Technique | App port |
|----------|-----------|-----------|----------|
| Node.js  | `node:20-alpine` | non-root, healthcheck | 3000 |
| Python   | `python:3.12-slim` | non-root user, slim base | 8000 |
| Java     | `eclipse-temurin:21` | multi-stage JDK → JRE | 8080 |
| Go       | `golang:1.22` → distroless | multi-stage, static binary | 8080 |
| PHP      | `php:8.3-apache` | front-controller routing | 80 |

### Build and run any example

```bash
# From the repository root, pick a language directory:
cd examples/nodejs        # or python, java, go, php

# Build the image
docker build -t dc-example-nodejs .

# Run it, publishing the container port to the host
docker run -d --name demo -p 3000:3000 dc-example-nodejs

# Verify
curl http://localhost:3000/          # -> Hello from a production-grade ... container!
curl http://localhost:3000/health    # -> {"status":"ok"}

# Inspect and clean up
docker logs demo
docker rm -f demo
```

Ports per example: Node.js `3000`, Python `8000`, Java `8080`, Go `8080`,
PHP `80`. Adjust the `-p host:container` mapping accordingly.

## Repository layout

```
.
├── README.md
├── docker commands.txt          # original cheatsheet
├── docs/
│   ├── docker-commands.md        # command reference
│   └── best-practices.md         # interview + production best practices
└── examples/
    ├── nodejs/   { Dockerfile, .dockerignore, package.json, server.js }
    ├── python/   { Dockerfile, .dockerignore, requirements.txt, app.py }
    ├── java/     { Dockerfile, .dockerignore, Main.java }
    ├── go/       { Dockerfile, .dockerignore, go.mod, main.go }
    └── php/      { Dockerfile, .dockerignore, index.php }
```

## Validation

All five example images were built with `docker build` and smoke-tested by
running the container and curling `/` and `/health` — every image builds
successfully and serves both endpoints.
