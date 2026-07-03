<?php
// Minimal PHP endpoint for the Docker example. Served by the built-in Apache
// module in the official php:apache image. No Composer dependencies required.

if (($_SERVER['REQUEST_URI'] ?? '/') === '/health') {
    header('Content-Type: application/json');
    echo json_encode(['status' => 'ok']);
    exit;
}

header('Content-Type: text/plain');
echo "Hello from a production-grade PHP container!\n";
