# syntax=docker/dockerfile:1

# Uses the official php-fpm + a lightweight built-in server for the example.
# For real apps, install extensions with docker-php-ext-install and run
# php-fpm behind nginx.
FROM php:8.3-cli-alpine AS runtime
WORKDIR /var/www/html

# Example: install common production extensions (kept minimal here).
# RUN docker-php-ext-install pdo pdo_mysql opcache

# Copy application source.
COPY . .

# Run as the unprivileged www-data user shipped in the base image.
USER www-data

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD php -r "exit(@file_get_contents('http://127.0.0.1:8080/health') !== false ? 0 : 1);"

# Built-in server is fine for demos; use php-fpm+nginx for production traffic.
CMD ["php", "-S", "0.0.0.0:8080", "index.php"]
