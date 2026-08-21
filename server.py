#!/usr/bin/env python3
"""
ChronoCanvas Local Runnable Server & HTTP API Gateway Bridge.
Serves static frontend files and bridges HTTP requests to the ChronoCanvas backend agent.
"""

import os
import sys
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Import backend agent module
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))
from agent import ChronoCanvasAgent

agent = ChronoCanvasAgent()

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")


class ChronoCanvasRequestHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def do_GET(self):
        if self.path == "/canvas/latest":
            self.send_json_response(agent.get_latest_canvas())
        elif self.path == "/canvas/history":
            self.send_json_response(agent.get_history())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/canvas/generate":
            new_canvas = agent.execute_autonomous_cycle()
            self.send_json_response(new_canvas, status=201)
        else:
            self.send_json_response({"error": "Not Found"}, status=404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))


def run_server(port=8085):
    print("=" * 65)
    print(f"[ChronoCanvas Server] Starting at http://localhost:{port}")
    print("=" * 65)

    # Initial autonomous trigger on server boot
    print("[Boot] Executing initial autonomous agent cycle...")
    agent.get_latest_canvas()

    server_address = ("", port)
    httpd = HTTPServer(server_address, ChronoCanvasRequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down ChronoCanvas server.")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8085
    run_server(port)
