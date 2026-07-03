<?php
// Minimal PHP entrypoint for the Docker example, served by php-fpm + nginx.
if (($_SERVER['REQUEST_URI'] ?? '/') === '/health') {
    header('Content-Type: application/json');
    echo json_encode(['status' => 'ok']);
    exit;
}

header('Content-Type: text/plain');
echo "Hello from a production-grade PHP container!\n";
