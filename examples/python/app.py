"""Minimal, dependency-free HTTP service for the Python Docker example.

Uses only the standard library so the image builds fully offline and stays
small. In a real project you would typically add a framework (Flask, FastAPI)
and pin it in requirements.txt.
"""
import json
import os
import signal
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "8000"))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 (stdlib naming)
        if self.path == "/health":
            body = json.dumps({"status": "ok"}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
        else:
            body = b"Hello from a production-grade Python container!\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        # Route access logs to stdout so `docker logs` captures them.
        sys.stdout.write("%s - %s\n" % (self.address_string(), args[0] % args[1:]))


def main():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)

    def shutdown(signum, _frame):
        print(f"Received signal {signum}, shutting down.")
        server.shutdown()

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    print(f"Python server listening on port {PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
