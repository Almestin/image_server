#!/usr/bin/env python3
# shebang

import re
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
            self.wfile.write(b"404 - Sorry, Not Found")

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path != "/upload":
            self.send_response(404)
            self.end_headers()
            return

        content_type = self.headers.get('Content-Type')
        if not content_type or not content_type.startswith('multipart/form-data'):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Expected multipart/form-data")
            return


        match = re.search(r'boundary=([^;]+)', content_type)
        if not match:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Boundary not found")
            return
        boundary = match.group(1).encode('utf-8')
        # add prefix
        boundary = b'--' + boundary

        # read request
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        parts = body.split(boundary)
        file_data = None
        original_filename = None

        for part in parts:
            # find filename=
            if b'filename="' in part:
                # Извлекаем имя файла
                fn_match = re.search(rb'filename="([^"]+)"', part)
                if fn_match:
                    original_filename = fn_match.group(1).decode('utf-8')

                # find start of data
                data_start = part.find(b'\r\n\r\n')
                if data_start != -1:
                    file_data = part[data_start + 4:]

                    if file_data.endswith(b'\r\n'):
                        file_data = file_data[:-2]
                    break

        if not file_data or not original_filename:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing file field 'file'")
            return

        ####  Temporary for test
        response_text = f"Received file: {original_filename}, size: {len(file_data)}"
        self.send_response(200)
        self.end_headers()
        self.wfile.write(response_text.encode())

def run_server(port=8000):
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, ImageHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()