# syntax=docker/dockerfile:1

# ---- Build stage -------------------------------------------------------------
FROM golang:1.22-alpine AS build
WORKDIR /src

# Copy module files first for dependency caching.
COPY go.mod ./
RUN go mod download

# Copy source and build a static binary.
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /out/app .

# ---- Runtime stage -----------------------------------------------------------
# Distroless static image: no shell, no package manager, tiny attack surface.
FROM gcr.io/distroless/static-debian12:nonroot
WORKDIR /app
COPY --from=build /out/app /app/app

USER nonroot:nonroot
ENV PORT=8080
EXPOSE 8080

ENTRYPOINT ["/app/app"]
