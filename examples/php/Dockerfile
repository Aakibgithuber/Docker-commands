# syntax=docker/dockerfile:1

# ---- PHP production image ----------------------------------------------------
# Official PHP with Apache; pin the minor version.
FROM php:8.3-apache

# Use the production php.ini and enable mod_rewrite (common real-world need).
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini" \
    && a2enmod rewrite

# Route every request through index.php (front-controller pattern) so app code
# handles paths like /health instead of Apache returning 404 for missing files.
RUN printf 'FallbackResource /index.php\n' > /etc/apache2/conf-enabled/fallback.conf

# Copy application into Apache's document root.
COPY index.php /var/www/html/

# The base image already runs Apache as the unprivileged www-data user.
EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD php -r "exit(@file_get_contents('http://127.0.0.1/health') !== false ? 0 : 1);"

# Base image's default CMD (apache2-foreground) starts the server.
