# Docker Commands Reference

A practical reference to the Docker commands you use most often, grouped by
topic, with explanations and real-world notes. Each section covers what the
command does, common flags, and when you would reach for it.

---

## 1. `docker build` — build an image from a Dockerfile

```bash
docker build -t myapp:1.0 .
docker build -t myapp:1.0 -f docker/Dockerfile .
docker build --no-cache -t myapp:1.0 .
docker build --target builder -t myapp-builder .
docker build --build-arg NODE_ENV=production -t myapp:1.0 .
```

| Flag | Meaning |
|------|---------|
| `-t name:tag` | Name and tag the resulting image. |
| `-f path` | Use a Dockerfile at a non-default path. |
| `--no-cache` | Ignore the build cache (force a clean build). |
| `--target` | Stop at a specific stage in a multi-stage build. |
| `--build-arg` | Pass a build-time variable (`ARG`). |

**Notes**
- The final `.` is the *build context* — the directory sent to the daemon.
  Keep it small with a `.dockerignore` file.
- Order Dockerfile layers from least to most frequently changing to maximise
  cache hits (copy dependency manifests before source code).

---

## 2. `docker run` — create and start a container

```bash
docker run hello-world                     # run once and exit
docker run -d --name web -p 8080:80 nginx  # detached, mapped port
docker run -it ubuntu /bin/bash            # interactive shell
docker run --rm alpine echo "hi"           # auto-remove on exit
docker run -e ENV=prod -e PORT=3000 myapp  # environment variables
docker run --env-file .env myapp           # env vars from a file
docker run --memory=512m --cpus=1.5 myapp  # resource limits
docker run --restart=unless-stopped myapp  # restart policy
```

| Flag | Meaning |
|------|---------|
| `-d` | Detached (run in background). |
| `-it` | Interactive + TTY (for shells). |
| `-p host:container` | Publish a container port to the host. |
| `--name` | Give the container a stable name. |
| `--rm` | Remove the container when it exits. |
| `-e` / `--env-file` | Set environment variables. |
| `-v` / `--mount` | Attach volumes / bind mounts. |
| `--restart` | Restart policy (`no`, `on-failure`, `always`, `unless-stopped`). |
| `--memory` / `--cpus` | Hard resource limits. |

**Notes**
- Prefer `--rm` for one-off/dev containers so they don't pile up.
- Always set resource limits in production to avoid noisy-neighbour issues.

---

## 3. `docker exec` — run a command in a running container

```bash
docker exec -it web /bin/bash        # open a shell inside a container
docker exec web ls /app              # run a one-off command
docker exec -u root web whoami       # run as a specific user
docker exec -e DEBUG=1 web env       # set an env var for the command
```

**Notes**
- `exec` runs a *new* process in an *already-running* container. Use it to
  debug live containers.
- If the container has no shell (e.g. `distroless`/`scratch` images), `exec`
  into a shell will fail by design — debug with `docker logs`, ephemeral
  debug containers, or `docker cp` instead.

---

## 4. `docker logs` — read container output

```bash
docker logs web                 # all logs so far
docker logs -f web              # follow (stream) new logs
docker logs --tail 100 web      # last 100 lines
docker logs --since 10m web     # logs from the last 10 minutes
docker logs -t web              # include timestamps
```

**Notes**
- `logs` reads whatever the main process writes to **stdout/stderr**. Apps in
  containers should log to stdout/stderr, not to files.
- For production, ship logs to a central system via a logging driver
  (`--log-driver=json-file|journald|awslogs|fluentd`) and cap size with
  `--log-opt max-size=10m --log-opt max-file=3`.

---

## 5. Volumes — persist and share data

Containers are ephemeral; volumes keep data alive across restarts.

```bash
docker volume create appdata            # create a named volume
docker volume ls                        # list volumes
docker volume inspect appdata           # details (mountpoint, driver)
docker volume rm appdata                # remove a volume
docker volume prune                     # remove all unused volumes

# Named volume (managed by Docker, best for databases):
docker run -d -v appdata:/var/lib/mysql mysql:8

# Bind mount (host path -> container, best for local dev):
docker run -d -v "$(pwd)":/app node:20-alpine

# Read-only mount:
docker run -v appdata:/data:ro myapp

# Preferred modern syntax:
docker run --mount type=volume,src=appdata,dst=/data myapp
docker run --mount type=bind,src="$(pwd)",dst=/app myapp
```

| Type | Use case |
|------|----------|
| **Named volume** | Databases and app state — Docker manages the storage. |
| **Bind mount** | Live-reloading source code during local development. |
| **tmpfs** | Sensitive/temporary data kept only in memory. |

**Notes**
- Never store important data only inside a container's writable layer — it is
  lost when the container is removed.
- `docker volume prune` deletes data permanently; be careful in shared envs.

---

## 6. Networking — connect containers

```bash
docker network ls                            # list networks
docker network create appnet                 # create a user-defined bridge
docker network inspect appnet                # inspect (subnet, containers)
docker network connect appnet web            # attach a running container
docker network disconnect appnet web         # detach
docker run -d --name db --network appnet postgres:16
docker run -d --name api --network appnet myapi   # api can reach "db" by name
```

**Network drivers**

| Driver | Use case |
|--------|----------|
| `bridge` (default) | Single-host container-to-container networking. |
| `host` | Share the host network stack (no port mapping, max perf). |
| `none` | Fully isolated, no networking. |
| `overlay` | Multi-host networking (Swarm / orchestration). |

**Notes**
- On a **user-defined bridge network**, containers resolve each other by
  **container name** via Docker's built-in DNS — this is the standard way to
  wire an app to its database. The default `bridge` network does *not* provide
  name resolution, so always create your own network.
- `-p 8080:80` publishes a port to the host; container-to-container traffic on
  the same network does **not** need published ports.

---

## Quick housekeeping commands

```bash
docker ps                     # running containers
docker ps -a                  # all containers (incl. stopped)
docker images                 # local images
docker stop $(docker ps -q)   # stop all running containers
docker rm $(docker ps -aq)    # remove all containers
docker rmi $(docker images -q)# remove all images
docker system df              # disk usage by images/containers/volumes
docker system prune -a        # reclaim space (unused images/containers/nets)
docker inspect <name>         # full JSON metadata for a container/image
docker stats                  # live CPU/memory/IO per container
```

> ⚠️ `docker system prune -a` and the bulk `rm`/`rmi` commands are
> destructive. Double-check before running them outside a throwaway machine.
