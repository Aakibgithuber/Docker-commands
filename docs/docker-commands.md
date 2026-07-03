# Docker Commands Reference

A practical, explained reference for the Docker commands you use most often in
development and production. Each section explains *what* the command does, the
*flags that matter*, and *when you would reach for it*.

> Tip: run `docker <command> --help` for the full, authoritative flag list.

---

## 1. `docker build` — build an image from a Dockerfile

```bash
docker build -t myapp:1.0 .
```

- `-t name:tag` — name and tag the image. Tag meaningfully (`1.0`, a git SHA);
  avoid relying on `latest` in production.
- `.` — the *build context*: the directory sent to the daemon. Keep it small
  with a good `.dockerignore` (see best-practices.md).
- `-f path/to/Dockerfile` — use a Dockerfile that is not at the context root.
- `--build-arg KEY=value` — pass build-time variables (`ARG`).
- `--target stage` — build only up to a named stage in a multi-stage build.
- `--no-cache` — force a clean rebuild, ignoring the layer cache.

**Production notes**
- Order Dockerfile instructions from least- to most-frequently changing so the
  layer cache is reused (copy dependency manifests and install *before* copying
  source).
- Use multi-stage builds to keep build tools out of the final image.

---

## 2. `docker run` — create and start a container from an image

```bash
docker run -d --name web -p 8080:80 --restart unless-stopped nginx:1.27
```

- `-d` — detached (background). Omit it (or use `-it`) to stay attached.
- `-it` — interactive + TTY, e.g. `docker run -it ubuntu /bin/bash`.
- `--name web` — give the container a stable name instead of a random one.
- `-p HOST:CONTAINER` — publish a container port to the host (`-p 8080:80`).
- `-e KEY=value` / `--env-file .env` — inject environment variables.
- `-v name:/path` or `-v /host:/container` — mount a volume or bind mount.
- `--restart unless-stopped` — restart policy for resilience.
- `--rm` — auto-remove the container when it exits (great for one-off tasks).
- `--network mynet` — attach to a specific network.

**Production notes**
- Prefer `--env-file` / secrets managers over baking secrets into images.
- Set resource limits: `--memory 512m --cpus 1.0`.

---

## 3. `docker exec` — run a command inside a running container

```bash
docker exec -it web /bin/bash
```

- `-it` — get an interactive shell.
- `docker exec web env` — run a one-off command (here, print env vars).
- `-u root` — run as a specific user.
- `-w /app` — set the working directory for the command.

**When to use:** debugging a live container, inspecting logs/config, running
migrations. `exec` runs a *new* process; `attach` connects to the main process.

---

## 4. `docker logs` — read a container's stdout/stderr

```bash
docker logs -f --tail 100 web
```

- `-f` — follow (stream) new log lines.
- `--tail N` — show only the last N lines.
- `--since 10m` / `--until 2024-01-01` — time-bound the output.
- `-t` — prefix each line with a timestamp.

**Production notes**
- Applications should log to **stdout/stderr** so Docker (and your log driver:
  json-file, journald, awslogs, etc.) can collect them.
- Configure log rotation (`--log-opt max-size=10m --log-opt max-file=3`) to
  avoid filling the disk.

---

## 5. Volumes — persistent and shared data

Containers are ephemeral; volumes are how data survives restarts.

```bash
docker volume create appdata
docker run -v appdata:/var/lib/app myapp        # named volume (managed by Docker)
docker run -v "$(pwd)":/src myapp               # bind mount (host path)
docker run --mount type=tmpfs,dst=/tmp myapp    # tmpfs (in-memory)
```

Useful commands:

| Command | Purpose |
| --- | --- |
| `docker volume ls` | List volumes |
| `docker volume inspect appdata` | Show a volume's details/mountpoint |
| `docker volume rm appdata` | Remove a volume |
| `docker volume prune` | Remove all unused volumes |

- **Named volumes** — Docker-managed, portable, best for databases.
- **Bind mounts** — map a host directory, great for local development.
- **tmpfs** — in-memory only, for sensitive or throwaway data.

---

## 6. Networking — how containers talk

```bash
docker network create appnet
docker run -d --name db  --network appnet postgres:16
docker run -d --name api --network appnet -p 8080:8080 myapi
```

- Containers on the **same user-defined bridge network** reach each other by
  **container name** as a DNS hostname (here, the API connects to `db:5432`).
- `-p HOST:CONTAINER` publishes a port to the outside world.
- Network drivers: `bridge` (default, single host), `host` (share the host's
  network stack), `overlay` (multi-host / Swarm), `none` (no networking).

Useful commands:

| Command | Purpose |
| --- | --- |
| `docker network ls` | List networks |
| `docker network inspect appnet` | Show connected containers, subnet |
| `docker network connect appnet web` | Attach a running container |
| `docker network prune` | Remove unused networks |

**Production notes**
- Put each app stack on its own user-defined network for isolation and DNS.
- Only publish the ports you actually need to expose.

---

## Quick housekeeping

```bash
docker ps -a                       # all containers (running + stopped)
docker images                      # local images
docker stop $(docker ps -a -q)     # stop every container
docker rm  $(docker ps -a -q)      # remove every container
docker rmi -f $(docker images -q)  # remove every image
docker system prune -a --volumes   # reclaim disk (careful: destructive)
```
