<?php
// Minimal PHP front controller demonstrating a production-grade PHP Docker image.
$path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH);

if ($path === '/health') {
    header('Content-Type: application/json');
    echo json_encode(['status' => 'ok']);
    exit;
}

echo "Hello from a containerized PHP app!\n";
