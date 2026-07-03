# Docker Commands, Documentation & Examples

Production-grade Docker reference material and ready-to-build example images.

This repository collects the Docker commands you use day to day, explains the
concepts behind them, captures common interview questions, and ships minimal
but **production-styled Dockerfiles** for five popular stacks.

## Repository structure

```
.
├── README.md                     # you are here
├── docker commands.txt           # original quick command cheat-sheet
├── docs/
│   ├── docker-commands.md        # build / run / exec / logs / volumes / networking
│   └── best-practices.md         # production best practices + interview Q&A
└── examples/                     # minimal, buildable, non-root images
    ├── nodejs/                   # Node.js 20 (multi-stage, alpine)
    ├── python/                   # Python 3.12 (venv, slim)
    ├── java/                     # Java 21 (JDK build -> JRE runtime)
    ├── go/                       # Go 1.22 (static binary -> distroless)
    └── php/                      # PHP 8.3 (cli-alpine)
```

## Documentation

- **[docs/docker-commands.md](docs/docker-commands.md)** — the core commands
  grouped by topic: `build`, `run`, `exec`, `logs`, volumes, and networking,
  each with flags, examples, and real-world notes.
- **[docs/best-practices.md](docs/best-practices.md)** — image, runtime, and
  security best practices, real production use cases, and a set of common
  Docker interview questions with answers.

## Example images

Every example is intentionally small and dependency-light so it builds
anywhere, and every one follows the same production practices:

- multi-stage builds (where the language benefits),
- small base images (`alpine` / `slim` / `distroless`),
- a non-root runtime user,
- a `.dockerignore`,
- a `/health` endpoint and a `HEALTHCHECK` (except the distroless Go image,
  which has no shell — health is checked by the orchestrator instead).

### Build & run any example

```bash
# Node.js
docker build -t example-node ./examples/nodejs
docker run --rm -p 3000:3000 example-node   # http://localhost:3000/health

# Python
docker build -t example-python ./examples/python
docker run --rm -p 8000:8000 example-python # http://localhost:8000/health

# Go
docker build -t example-go ./examples/go
docker run --rm -p 8080:8080 example-go     # http://localhost:8080/health

# Java
docker build -t example-java ./examples/java
docker run --rm -p 8080:8080 example-java   # http://localhost:8080/health

# PHP
docker build -t example-php ./examples/php
docker run --rm -p 8080:8080 example-php    # http://localhost:8080/health
```

Each server responds with a greeting on `/` and `{"status":"ok"}` on
`/health`.

## Verification

All five images were built and run locally with Docker; each container was
smoke-tested and returned `200 OK` from its `/health` endpoint. See the pull
request description for the exact build/run output.
