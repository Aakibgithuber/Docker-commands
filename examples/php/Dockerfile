# syntax=docker/dockerfile:1

# ---- Production PHP image (Apache + mod_php) ----
FROM php:8.3-apache

# Route all requests through the front controller (index.php).
COPY apache-app.conf /etc/apache2/conf-enabled/app.conf

# Copy application source into Apache's document root.
COPY index.php /var/www/html/

# Apache already runs worker processes as the non-root `www-data` user.
EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD php -r "exit(@file_get_contents('http://localhost/health') !== false ? 0 : 1);"

# The php:apache base image already sets CMD ["apache2-foreground"].
