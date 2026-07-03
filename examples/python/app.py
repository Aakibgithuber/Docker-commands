"""Minimal Flask app demonstrating a production-grade Python Docker image."""
import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return "Hello from a containerized Python app!\n"


@app.get("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
