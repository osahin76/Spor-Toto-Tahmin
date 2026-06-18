import http.server
import urllib.request
import urllib.error
import os

PORT = int(os.environ.get('PORT', 8000))
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, x-api-key, anthropic-version, anthropic-beta')
        self.end_headers()

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/SpotTotoTahmin.html'
        super().do_GET()

    def do_POST(self):
        if self.path == '/api/claude':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            # Gelen key'i kontrol et - boş, __server__ veya geçersizse env'den kullan
            client_key = self.headers.get('x-api-key', '').strip()
            if not client_key or client_key == '__server__' or not client_key.startswith('sk-ant-'):
                api_key = ANTHROPIC_API_KEY
            else:
                api_key = client_key
            beta = self.headers.get('anthropic-beta', '')
            req = urllib.request.Request(
                'https://api.anthropic.com/v1/messages',
                data=body,
                headers={
                    'Content-Type': 'application/json',
                    'x-api-key': api_key,
                    'anthropic-version': '2023-06-01',
                    'anthropic-beta': beta
                },
                method='POST'
            )
            try:
                with urllib.request.urlopen(req) as resp:
                    result = resp.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(result)
            except urllib.error.HTTPError as e:
                result = e.read()
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(result)
        else:
            super().do_POST()

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"Spor Toto Tahmin: http://0.0.0.0:{PORT}")
print(f"API Key: {'✓ ENV aktif' if ANTHROPIC_API_KEY else '✗ ENV bos'}")
httpd = http.server.HTTPServer(('0.0.0.0', PORT), Handler)
httpd.serve_forever()
