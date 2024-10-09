from http.server import BaseHTTPRequestHandler, HTTPServer
from main.model.figcheck import figcheck, set_up
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

tokenizer, model = set_up()

class RequestHandler(BaseHTTPRequestHandler):
    
    def _set_headers(self, status_code=200, content_type='application/json'):
        """Set common headers to allow CORS and JSON content"""
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow cross-origin requests
        self.end_headers()

    def do_HEAD(self):
        """Handle HEAD requests - just return headers, no body."""
        self._set_headers(content_type='text/html')

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/get_text':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            try:
                data = json.loads(post_data)
                text_input = data.get('text_input', '')

                if text_input:
                    result = figcheck(text_input, tokenizer, model)

                    # Log the received input and model's predictions
                    logging.info(f"Received Input: {text_input}")
                    logging.info(f"Grammar Predictions: {result['grammar_predictions']}")

                    self._set_headers()
                    self.wfile.write(json.dumps(result).encode('utf-8'))
                else:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({"error": "No text_input provided"}).encode('utf-8'))

            except json.JSONDecodeError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode('utf-8'))

    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/':
            self._set_headers(content_type='text/html')
            with open('main/index.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path.endswith('.css'):
            self._set_headers(content_type='text/css')
            css_file_path = 'main/assets/' + self.path.split('/')[-1]
            with open(css_file_path, 'rb') as f:
                self.wfile.write(f.read())
        elif self.path.endswith('.js'):
            self._set_headers(content_type='application/javascript')
            js_file_path = 'main/assets/' + self.path.split('/')[-1]
            with open(js_file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()