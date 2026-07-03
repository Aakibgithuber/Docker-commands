# syntax=docker/dockerfile:1

# ---- Build stage -------------------------------------------------------------
# Compile with a full JDK, then ship only the JRE runtime.
FROM eclipse-temurin:21-jdk-alpine AS build
WORKDIR /src
COPY Main.java ./
RUN javac -d /out Main.java

# ---- Runtime stage -----------------------------------------------------------
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=build /out ./

# Run as a non-root user.
RUN addgroup -S app && adduser -S -G app app
USER app

ENV PORT=8080
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget -qO- http://127.0.0.1:8080/health || exit 1

CMD ["java", "Main"]
