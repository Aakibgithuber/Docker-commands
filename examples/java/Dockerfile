# syntax=docker/dockerfile:1

# ---- Build stage: compile with the full JDK ----
FROM eclipse-temurin:21-jdk AS build
WORKDIR /src
COPY Main.java ./
RUN javac Main.java

# ---- Runtime stage: ship only the JRE + compiled classes ----
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /src/Main.class ./

# Run as a non-root user.
RUN useradd --create-home --uid 1001 appuser
USER appuser

ENV PORT=8080
EXPOSE 8080

CMD ["java", "Main"]
