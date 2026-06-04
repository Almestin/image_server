#!/usr/bin/env python3
# shebang

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

class ImageHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            message = (
                "Welcome to the image hosting service!\n"
                "Use POST /upload to upload an image.\n"
                "Uploaded images are available at: http://localhost:8080/images/<filename>\n"
            )
            self.wfile.write(message.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

def run_server():
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, ImageHandler)
    print("Server running on port 8000")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()