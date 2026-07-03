# syntax=docker/dockerfile:1

# ---- Stage 1: compile sources and package a runnable jar ----
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /build

COPY src ./src
RUN mkdir -p out && \
    javac -d out $(find src -name '*.java') && \
    echo "Main-Class: com.example.App" > out/manifest.txt && \
    jar --create --file app.jar --manifest out/manifest.txt -C out com

# ---- Stage 2: minimal JRE runtime ----
FROM eclipse-temurin:21-jre-alpine AS runtime
WORKDIR /app

# Run as a non-root user.
RUN addgroup -S app && adduser -S -G app app
COPY --from=builder /build/app.jar ./app.jar
USER app

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://127.0.0.1:8080/health || exit 1

CMD ["java", "-jar", "app.jar"]
