# Jenkins Hello World Pipeline

A small, beginner-friendly example that shows how a Jenkins pipeline can build a
Docker image and push it to Docker Hub.

## What's here

| File | Purpose |
| ---- | ------- |
| [`../Jenkinsfile`](../Jenkinsfile) | Declarative pipeline with commented stages. |
| `Dockerfile` | Minimal Alpine image that prints a "Hello, World!" message. |

## Pipeline stages

1. **Checkout** – pull the source code from the repository.
2. **Build Image** – build the Docker image from `jenkins-hello-world/Dockerfile`, tagged with the build number and `latest`.
3. **Test Image** – run the image once to confirm it works.
4. **Login to Docker Hub** – authenticate using stored Jenkins credentials.
5. **Push Image** – push both tags to Docker Hub.
6. **Post / cleanup** – log out and remove the local images.

## One-time Jenkins setup

1. Make sure the Jenkins agent has Docker installed and the `docker` CLI available.
2. In **Manage Jenkins → Credentials**, add a **Username with password** credential:
   - **ID:** `dockerhub-credentials`
   - **Username:** your Docker Hub username
   - **Password:** a Docker Hub [access token](https://hub.docker.com/settings/security) (recommended) or your password
3. Create a **Pipeline** job that points at this repository and uses the root `Jenkinsfile`.
4. In the `Jenkinsfile`, set `DOCKERHUB_USER` to your own Docker Hub username.

## Run it locally (optional)

You can build and run the same image without Jenkins:

```bash
cd jenkins-hello-world
docker build -t hello-world-jenkins .
docker run --rm hello-world-jenkins
# -> Hello, World! This image was built and pushed by a Jenkins pipeline.
```
