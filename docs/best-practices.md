# Docker Best Practices — Interview & Production

A condensed, practical guide covering the questions that come up in interviews
and the practices that matter when you run containers in production.

---

## Image building

1. **Use small, specific base images.** Prefer `-slim`, `-alpine`, or
   distroless over full `latest` images. Pin versions (`node:20-alpine`, not
   `node:latest`) for reproducible builds.
2. **Use multi-stage builds.** Compile in a build stage with the full toolchain,
   then copy only the artifact into a minimal runtime image. This is how the
   Go and Java examples in this repo ship tiny final images.
3. **Order layers from least- to most-frequently changed.** Copy dependency
   manifests (`package.json`, `requirements.txt`, `go.mod`) and install
   *before* copying source, so the dependency layer stays cached.
4. **Keep the build context small** with `.dockerignore` (exclude `.git`,
   `node_modules`, build output, secrets).
5. **Minimize layers and clean up in the same `RUN`.** e.g.
   `apt-get update && apt-get install -y x && rm -rf /var/lib/apt/lists/*`.
6. **Leverage the build cache**, but use `--no-cache` in CI when you need a
   guaranteed-fresh build.

## Security

1. **Run as a non-root user.** Create an unprivileged user and `USER` it. Every
   example in this repo drops root.
2. **Never bake secrets into images.** Pass them at runtime via environment
   variables, Docker secrets, or a secrets manager. Anything in a layer is
   recoverable from the image.
3. **Scan images for vulnerabilities** (`docker scout cves`, Trivy, Grype) in CI.
4. **Use trusted, pinned base images**, ideally by digest (`image@sha256:...`)
   for immutability.
5. **Drop capabilities and avoid `--privileged`.** Add only the capabilities you
   need (`--cap-drop=ALL --cap-add=...`).
6. **Make the root filesystem read-only** where possible (`--read-only`) and
   mount writable paths as `tmpfs` or volumes.

## Runtime & operations

1. **Log to stdout/stderr**, not to files — the platform collects them and
   `docker logs` works out of the box.
2. **One concern per container.** A container should run a single main process
   (PID 1). Use an init (`--init`) if you need proper signal/zombie handling.
3. **Handle signals for graceful shutdown.** Trap `SIGTERM` so in-flight work
   finishes (all example apps here do this).
4. **Add a `HEALTHCHECK`** so orchestrators know when a container is ready and
   healthy.
5. **Set resource limits** (`--memory`, `--cpus`) to protect the host.
6. **Use restart policies** (`--restart unless-stopped`) for resilience.
7. **Treat containers as immutable and disposable** — rebuild and redeploy
   rather than patching a running container.

## Data & configuration

1. **Persist state in named volumes**, never inside the container's writable
   layer.
2. **Configure via environment variables** (12-factor). Keep images
   environment-agnostic and inject config at runtime.
3. **Externalize databases and caches** — they usually should not live in the
   same lifecycle as your app container.

---

## Common interview questions (quick answers)

**Image vs. container?** An image is an immutable, layered template; a container
is a running (or stopped) instance of an image with a writable top layer.

**`CMD` vs. `ENTRYPOINT`?** `ENTRYPOINT` sets the executable that always runs;
`CMD` provides default arguments (or the default command). With an `ENTRYPOINT`,
`CMD` becomes its default args, which you can override on `docker run`.

**`COPY` vs. `ADD`?** Use `COPY` for plain files/directories. `ADD` also
auto-extracts local tar archives and can fetch URLs — prefer `COPY` unless you
specifically need those features.

**`RUN` vs. `CMD` vs. `ENTRYPOINT`?** `RUN` executes at **build** time and
creates a layer. `CMD`/`ENTRYPOINT` define what runs at **container start**.

**Why are my container's changes gone after restart?** The writable layer of a
removed container is discarded. Persist data in a **volume**.

**How do containers talk to each other?** Put them on the same user-defined
network and reference each other by container name (Docker DNS).

**Bind mount vs. volume?** A bind mount maps a host path (great for dev); a named
volume is Docker-managed storage (preferred for portable, persistent data).

**How do you make images smaller?** Smaller base image, multi-stage builds,
fewer/combined layers, remove build tools and caches, `.dockerignore`.

**Why not run as root?** A container escape as root maps to elevated privileges;
running as a non-root user limits the blast radius.

**What is a layer and how is the cache used?** Each instruction can create a
layer; Docker reuses cached layers until an instruction (or its inputs) changes,
then rebuilds that layer and everything after it.

---

## Real-world production checklist

- [ ] Pinned, minimal base image (ideally by digest)
- [ ] Multi-stage build; no build tools in the final image
- [ ] `.dockerignore` present and effective
- [ ] Runs as non-root
- [ ] No secrets in the image; config via env/secrets manager
- [ ] `HEALTHCHECK` defined
- [ ] Graceful `SIGTERM` handling
- [ ] Logs to stdout/stderr
- [ ] Resource limits and restart policy set at deploy time
- [ ] Image scanned for CVEs in CI
- [ ] Tagged with an immutable version (not just `latest`)
