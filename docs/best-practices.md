# Docker Best Practices & Interview Notes

Production-oriented guidance plus the questions that come up in interviews.
Pair this with the runnable examples under [`examples/`](../examples).

---

## Image-building best practices

1. **Use small, specific base images.** Prefer `-slim` or `-alpine` variants and
   pin a version (`python:3.12-slim`, not `python:latest`). Smaller images pull
   faster and have a smaller attack surface.
2. **Use multi-stage builds.** Compile/build in a heavy stage, copy only the
   artifact into a minimal runtime stage. See the Go and Java examples.
3. **Optimize layer caching.** Copy dependency manifests and install
   dependencies *before* copying the rest of the source, so code changes don't
   invalidate the dependency layer.
4. **Minimize layers and clean up in the same layer.** e.g.
   `RUN apt-get update && apt-get install -y x && rm -rf /var/lib/apt/lists/*`.
5. **Add a `.dockerignore`.** Keep `.git`, `node_modules`, build output, and
   secrets out of the build context — faster builds, no accidental leaks.
6. **Run as a non-root user.** Create a dedicated user and `USER` it. Limits the
   blast radius if the app is compromised.
7. **Set a `HEALTHCHECK`.** Lets Docker/orchestrators know when a container is
   actually ready and healthy.
8. **Be explicit about `EXPOSE`, `ENV`, and `CMD`/`ENTRYPOINT`.** Use
   `ENTRYPOINT` for the fixed executable and `CMD` for default arguments.
9. **Don't bake secrets into images.** Use build secrets, runtime env vars, or a
   secrets manager. Anyone who pulls the image can read baked-in layers.
10. **Pin and scan.** Pin base image digests where it matters and scan images
    (`docker scout`, Trivy) in CI.

---

## Runtime best practices

- **Log to stdout/stderr** and let the platform collect logs; configure rotation.
- **Set resource limits** (`--memory`, `--cpus`) to protect the host.
- **Use restart policies** (`--restart unless-stopped`) for resilience.
- **Prefer named volumes** for stateful data; treat containers as disposable.
- **One concern per container.** Run the app; use separate containers for the
  database, cache, etc., wired together on a user-defined network.
- **Handle signals.** Ensure your process is PID 1-friendly or use
  `--init` so `SIGTERM` leads to a graceful shutdown.

---

## Common interview questions

**Image vs. container?**
An image is an immutable, layered template; a container is a running (or stopped)
instance of an image with a writable layer on top.

**`COPY` vs. `ADD`?**
Use `COPY` for plain file copies. `ADD` additionally auto-extracts local tar
archives and can fetch URLs — prefer `COPY` unless you need those behaviors.

**`CMD` vs. `ENTRYPOINT`?**
`ENTRYPOINT` sets the executable that always runs; `CMD` provides default
arguments (or the default command). Combined, `ENTRYPOINT ["nginx"]` +
`CMD ["-g","daemon off;"]` runs nginx but lets you override the args.

**`RUN` vs. `CMD` vs. `ENTRYPOINT`?**
`RUN` executes at **build** time and creates a new layer. `CMD`/`ENTRYPOINT`
define what runs at **container start**.

**What makes an image layer, and why does ordering matter?**
Each instruction (`RUN`, `COPY`, `ADD`) creates a cached layer. Put stable
instructions first so frequent code changes reuse the cached dependency layers.

**Bind mount vs. named volume?**
A bind mount maps a specific host path (good for dev). A named volume is managed
by Docker in its storage area (good for portable, production state).

**How do two containers communicate?**
Attach them to the same user-defined network and reference each other by
container name (Docker's embedded DNS resolves it).

**Why multi-stage builds?**
They keep compilers, dev dependencies, and build caches out of the final image,
producing a much smaller and more secure runtime image.

**How do you reduce image size?**
Slim/alpine base, multi-stage builds, `.dockerignore`, combine and clean up
`RUN` layers, remove caches, and avoid installing unnecessary packages.

**How do you keep containers secure?**
Non-root user, minimal base image, no secrets in layers, pin/scan images, drop
capabilities, read-only root filesystem where possible, and keep bases patched.
