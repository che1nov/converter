from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
import os

from currency_converter import CurrencyConverter
from history_manager import HistoryManager


class SimpleServer(BaseHTTPRequestHandler):
    converter = CurrencyConverter()
    history = HistoryManager()

    def _set_headers(self, content_type="text/html", status=200):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        try:
            if path == '/convert':
                query = parse_qs(parsed_url.query)
                amount = float(query.get('amount', [None])[0])
                from_curr = query.get('from', [None])[0].upper()
                to_curr = query.get('to', [None])[0].upper()

                result = self.converter.convert(amount, from_curr, to_curr)
                operation = {
                    "amount": amount,
                    "from": from_curr,
                    "to": to_curr,
                    "converted": result
                }
                self.history.add_operation(operation)

                self._set_headers("application/json")
                self.wfile.write(json.dumps(operation).encode())

            elif path == '/history':
                self._set_headers("application/json")
                self.wfile.write(json.dumps(self.history.get_operations()).encode())

            elif path == '/' or path == '/index.html':
                self._set_headers("text/html")

                current_dir = os.path.dirname(os.path.abspath(__file__))
                project_root = os.path.dirname(current_dir)
                file_path = os.path.join(project_root, "static", "index.html")

                print(f"[DEBUG] Trying to open: {file_path}") 

                try:
                    with open(file_path, "rb") as f:
                        self.wfile.write(f.read())
                except FileNotFoundError:
                    print("[ERROR] File not found")
                    self._set_headers(500)
                    self.wfile.write(b"Error: index.html not found")

            elif path == '/favicon.ico':
                self._set_headers("image/x-icon")
                self.wfile.write(b'')

            else:
                self._set_headers(404)
                self.wfile.write(b"404 Not Found")

        except Exception as e:
            print(f"[ERROR] {str(e)}")
            self._set_headers("application/json", 400)
            self.wfile.write(json.dumps({"error": str(e)}).encode())


def run(server_class=HTTPServer, handler_class=SimpleServer, port=8008):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
    