#!/usr/bin/env python3
# shebang

from http.server import HTTPServer, BaseHTTPRequestHandler

class ImageHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello from Image Hosting!")

def run_server():
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, ImageHandler)
    print("Server running on port 8000")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()