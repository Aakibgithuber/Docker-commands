# syntax=docker/dockerfile:1

# ---- Stage 1: compile a static binary ----
FROM golang:1.22-alpine AS builder
WORKDIR /src

# Cache module downloads separately from source builds.
COPY go.mod ./
RUN go mod download

COPY . .
# CGO disabled + static build so the binary runs on scratch.
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/server .

# ---- Stage 2: minimal runtime ----
FROM gcr.io/distroless/static-debian12:nonroot AS runtime
WORKDIR /app
COPY --from=builder /app/server /app/server
USER nonroot:nonroot

EXPOSE 8080
CMD ["/app/server"]
