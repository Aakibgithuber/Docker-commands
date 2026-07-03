# Docker Best Practices & Interview Notes

Production-focused guidance plus the questions that come up in interviews.
Everything here is applied concretely in the [`examples/`](../examples) folder.

---

## Image-building best practices

1. **Use small, official base images.** Prefer `-alpine`, `-slim`, or
   `distroless` variants. Smaller images = faster pulls, smaller attack
   surface. (Our Go example ships on `distroless/static`; Node/Python use
   `alpine`/`slim`.)

2. **Use multi-stage builds.** Compile/install in a heavy "builder" stage,
   then copy only the artifacts into a lean runtime stage. This keeps compilers
   and dev dependencies out of the final image.

3. **Pin versions.** Use explicit tags (`node:20-alpine`, `python:3.12-slim`),
   never `latest`, so builds are reproducible.

4. **Order layers for cache efficiency.** Copy dependency manifests
   (`package.json`, `requirements.txt`, `go.mod`) and install *before* copying
   application source. Source changes then don't invalidate the dependency
   layer.

5. **Use a `.dockerignore`.** Keep `node_modules`, `.git`, secrets, and build
   artifacts out of the build context. Faster builds, no accidental secret
   leaks. (Every example here has one.)

6. **Run as a non-root user.** Create/USE an unprivileged user so a container
   breakout doesn't hand over root. All five examples run as non-root.

7. **One process per container.** Design containers around a single concern;
   scale horizontally instead of cramming services together.

8. **Add a `HEALTHCHECK`.** Let the orchestrator know when the app is actually
   ready/alive, not just when the process exists.

9. **Combine `RUN` steps and clean up in the same layer** to avoid leaving
   caches behind:
   ```dockerfile
   RUN apt-get update && apt-get install -y --no-install-recommends curl \
       && rm -rf /var/lib/apt/lists/*
   ```

10. **Leverage BuildKit.** `# syntax=docker/dockerfile:1` plus cache mounts
    (`RUN --mount=type=cache,...`) speed up dependency installs dramatically.

---

## Runtime & production best practices

- **Set resource limits** (`--memory`, `--cpus`) so one container can't starve
  the host.
- **Set a restart policy** (`--restart=unless-stopped`) for long-running
  services.
- **Log to stdout/stderr** and let the platform aggregate logs; cap log size
  with `--log-opt max-size`/`max-file`.
- **Never bake secrets into images.** Pass them at runtime via env vars,
  Docker secrets, or a secrets manager. Secrets in image layers are permanent
  and extractable.
- **Make containers stateless.** Persist state in volumes or external
  services (databases, object storage) so containers stay disposable.
- **Scan images** for vulnerabilities (`docker scout cves`, Trivy, Grype) as
  part of CI.
- **Use user-defined networks** so services find each other by name and are
  isolated from unrelated containers.

---

## Real-world production use cases

- **CI/CD build agents** — reproducible, disposable build environments.
- **Microservices** — one image per service, wired together over an overlay
  network under Kubernetes/Swarm.
- **Database + app locally** — `docker compose up` to spin an app and its
  Postgres/MySQL with one command.
- **Golden runtime images** — a hardened base image per language that every
  team extends, centralising patching.
- **Ephemeral preview environments** — a container per pull request for QA.

---

## Common interview questions

**Q: Image vs. container?**
An image is a read-only template (layers) built from a Dockerfile. A container
is a running (or stopped) instance of an image with a thin writable layer on
top.

**Q: `COPY` vs. `ADD`?**
`COPY` just copies files. `ADD` also auto-extracts local tar archives and can
fetch URLs. Prefer `COPY` unless you specifically need `ADD`'s extraction.

**Q: `CMD` vs. `ENTRYPOINT`?**
`ENTRYPOINT` sets the executable that always runs; `CMD` provides default
arguments (or the default command). Use `ENTRYPOINT` for the binary and `CMD`
for overridable args. Prefer the exec form `["cmd","arg"]` over shell form.

**Q: `RUN` vs. `CMD` vs. `ENTRYPOINT`?**
`RUN` executes at **build time** and creates a new layer. `CMD`/`ENTRYPOINT`
define what runs at **container start**.

**Q: How do you make images smaller?**
Multi-stage builds, minimal base images (alpine/slim/distroless/scratch),
combine and clean up `RUN` layers, `.dockerignore`, and copy only needed
artifacts.

**Q: How do containers persist data?**
Named volumes (Docker-managed), bind mounts (host path), or tmpfs (memory).
The container's own writable layer is not durable.

**Q: How do two containers talk to each other?**
Put them on the same user-defined network and reference each other by
container name (Docker's embedded DNS resolves it).

**Q: What is a multi-stage build and why use it?**
A Dockerfile with multiple `FROM` stages; build artifacts are produced in one
stage and copied into a smaller final stage, keeping build tooling out of the
shipped image.

**Q: Why avoid `latest` in production?**
`latest` is a moving tag — builds become non-reproducible and can silently
pull a different, possibly breaking, image. Pin explicit versions.

**Q: How do you reduce the attack surface?**
Minimal base image, run as non-root, drop capabilities, read-only root
filesystem where possible, scan images, and keep bases patched.
