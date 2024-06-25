from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from openai import OpenAI

client = OpenAI()


class Handler(BaseHTTPRequestHandler):

    def response(self, code: int, content: str, content_type="text/plain"):
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", len(content))
        self.end_headers()
        self.wfile.write(content.encode())

    def _200(self, content: str, content_type: str = "text/plain"):
        self.response(200, content, content_type)

    def _json(self, content: dict):
        self._200(json.dumps(content), "application/json")

    def do_GET(self):
        self._200("Hello, World!")

    def do_POST(self):
        if self.path.startswith("/api"):
            ...
        self.response("Not Found", 404)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    server.serve_forever()
