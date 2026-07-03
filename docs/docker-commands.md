# Docker Commands Reference

A practical reference for the Docker commands you use most often, grouped by
task. Each command lists what it does, a common form, and the flags that matter
in real work.

> Tip: `docker <command> --help` always prints the authoritative flag list.

---

## 1. `docker build` — build an image from a Dockerfile

Builds an image from a `Dockerfile` and a *build context* (the directory sent to
the daemon).

```bash
# Build and tag an image from the current directory
docker build -t myapp:1.0 .

# Build a specific Dockerfile and target stage (multi-stage builds)
docker build -f docker/Dockerfile --target build -t myapp:build .

# Pass build-time variables and disable cache
docker build --build-arg NODE_ENV=production --no-cache -t myapp:1.0 .
```

Key flags:

| Flag | Purpose |
|------|---------|
| `-t name:tag` | Name and tag the image. Tag every build. |
| `-f path` | Use a Dockerfile that is not `./Dockerfile`. |
| `--target` | Stop at a named stage in a multi-stage build. |
| `--build-arg` | Pass an `ARG` value into the build. |
| `--no-cache` | Rebuild every layer, ignoring the cache. |

**Best practice:** keep the build context small with a `.dockerignore` file — a
large context (e.g. `node_modules`, `.git`) slows every build.

---

## 2. `docker run` — create and start a container

```bash
# Run interactively with a shell
docker run -it --name shell ubuntu:22.04 /bin/bash

# Run detached, publish a port, pass an env var, auto-remove on exit
docker run -d --name web -p 8080:80 -e NODE_ENV=production --rm myapp:1.0
```

Key flags:

| Flag | Purpose |
|------|---------|
| `-d` | Detached (run in the background). |
| `-it` | Interactive + TTY (for shells). |
| `--name` | Give the container a stable name. |
| `-p host:container` | Publish/map a port to the host. |
| `-e KEY=value` | Set an environment variable. |
| `-v vol:/path` | Mount a volume or bind mount. |
| `--rm` | Delete the container when it exits. |
| `--restart` | Restart policy (`no`, `on-failure`, `always`, `unless-stopped`). |

---

## 3. `docker exec` — run a command in a running container

```bash
# Open a shell inside a running container
docker exec -it web /bin/sh

# Run a one-off command (e.g. a DB migration) without a shell
docker exec web php artisan migrate --force
```

`exec` runs a *new* process inside an already-running container. Use it to
inspect state or run maintenance tasks. (`docker attach` instead connects to the
container's main process — usually not what you want.)

---

## 4. `docker logs` — read a container's output

```bash
docker logs web              # print all logs
docker logs -f web           # follow (stream) new logs
docker logs --tail 100 web   # last 100 lines
docker logs --since 10m web  # last 10 minutes, with timestamps
docker logs -t web
```

`docker logs` reads whatever the main process writes to **stdout/stderr** — this
is why production images should log to stdout/stderr rather than to files.

---

## 5. Volumes — persist and share data

Containers are ephemeral; volumes keep data alive across restarts and rebuilds.

```bash
# Named volume (managed by Docker) — preferred for persistent data
docker volume create appdata
docker run -d -v appdata:/var/lib/data myapp:1.0

# Bind mount (host path) — great for local development
docker run -d -v "$(pwd)":/app myapp:1.0

# Inspect and clean up
docker volume ls
docker volume inspect appdata
docker volume rm appdata
docker volume prune          # remove all unused volumes
```

| Type | Use case |
|------|----------|
| Named volume | Databases, uploads — persistent, portable, backed up. |
| Bind mount | Live-editing source during development. |
| `tmpfs` | Sensitive/scratch data kept only in memory. |

---

## 6. Networking — connect containers

```bash
# Create a user-defined bridge network (enables DNS by container name)
docker network create appnet

# Attach containers; they can now reach each other by name
docker run -d --name db --network appnet postgres:16
docker run -d --name api --network appnet -p 8080:8080 myapp:1.0
# 'api' can connect to the database at host 'db:5432'

# Inspect and clean up
docker network ls
docker network inspect appnet
docker network rm appnet
```

Notes:

- On a **user-defined** network, containers resolve each other by name via
  Docker's embedded DNS. The default `bridge` network does **not** provide this.
- `-p 8080:80` publishes a port to the host; container-to-container traffic on
  the same network does not need `-p`.
- Network modes: `bridge` (default), `host` (share the host stack), `none` (no
  networking).

---

## Quick lifecycle & housekeeping

```bash
docker ps                       # running containers
docker ps -a                    # all containers
docker images                   # local images
docker stop web && docker rm web
docker rmi myapp:1.0            # remove an image
docker system df               # disk usage
docker system prune -a         # remove unused data (careful!)
```
