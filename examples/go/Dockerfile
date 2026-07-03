# syntax=docker/dockerfile:1

# ---- Build stage: compile a static binary ----
FROM golang:1.22-alpine AS build
WORKDIR /src

# Cache modules first (only go.mod here since there are no external deps).
COPY go.mod ./
RUN go mod download

COPY . .
# CGO disabled => a fully static binary that runs on scratch.
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /out/server .

# ---- Runtime stage: tiny scratch image with just the binary ----
FROM scratch
COPY --from=build /out/server /server

ENV PORT=8080
EXPOSE 8080
USER 1001

ENTRYPOINT ["/server"]
