# Docker Commands, Documentation & Examples

Production-grade Docker reference material and runnable example Dockerfiles for
common language stacks. Useful both as a day-to-day cheat sheet and as
interview-preparation notes.

## Contents

| Path | What's inside |
| --- | --- |
| [`docs/docker-commands.md`](docs/docker-commands.md) | Explained reference for `build`, `run`, `exec`, `logs`, volumes, and networking. |
| [`docs/best-practices.md`](docs/best-practices.md) | Production best practices + common interview questions and answers. |
| [`examples/nodejs`](examples/nodejs) | Node.js app + production Dockerfile (non-root, healthcheck). |
| [`examples/python`](examples/python) | Python/Flask app + Dockerfile served with gunicorn. |
| [`examples/java`](examples/java) | Java app + multi-stage Dockerfile (JDK build → JRE runtime). |
| [`examples/go`](examples/go) | Go app + multi-stage Dockerfile (static binary → `scratch`). |
| [`examples/php`](examples/php) | PHP app + Dockerfile on `php:apache`. |
| [`docker commands.txt`](docker%20commands.txt) | Original quick command notes. |

Each example directory contains its own `Dockerfile` and `.dockerignore` and is
self-contained.

## Quick start

Build and run any example, e.g. the Node.js one:

```bash
cd examples/nodejs
docker build -t nodejs-example .
docker run --rm -p 3000:3000 nodejs-example
# in another terminal:
curl localhost:3000
curl localhost:3000/health
```

Port mapping per example:

| Example | Container port | Example run |
| --- | --- | --- |
| nodejs | 3000 | `docker run --rm -p 3000:3000 nodejs-example` |
| python | 8000 | `docker run --rm -p 8000:8000 python-example` |
| java   | 8080 | `docker run --rm -p 8080:8080 java-example` |
| go     | 8080 | `docker run --rm -p 8080:8080 go-example` |
| php    | 80   | `docker run --rm -p 8080:80 php-example` |

## Design principles used in the examples

- Small, version-pinned base images (`-slim` / `-alpine`).
- Multi-stage builds for compiled languages (Go, Java) to ship minimal runtimes.
- Dependency-manifest-first copy order for effective layer caching.
- Non-root runtime users where the base image allows it.
- A `.dockerignore` in every example to keep the build context lean.
- Healthchecks on the long-running web services.

See [`docs/best-practices.md`](docs/best-practices.md) for the reasoning behind
each of these.
