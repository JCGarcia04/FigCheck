from http.server import BaseHTTPRequestHandler, HTTPServer
from main.model.figcheck import figcheck, set_up
import json
import logging

# Configure logging (optional, but recommended for debugging)
logging.basicConfig(level=logging.INFO)

tokenizer, model = set_up()

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/get_text':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            try:
                data = json.loads(post_data)

                text_input = data.get('text_input', '')

                if text_input:
                    result = figcheck(text_input, tokenizer, model)

                    # Log the received input and the model's predictions
                    logging.info(f"Received Input: {text_input}")
                    logging.info(f"Grammar Predictions: {result['grammar_predictions']}")

                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(result).encode('utf-8'))

                else:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "No text_input provided"}).encode('utf-8'))

            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode('utf-8'))

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            with open('main/index.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path.endswith('.css'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/css')
            self.end_headers()
            css_file_path = 'main/assets/' + self.path.split('/')[-1]
            with open(css_file_path, 'rb') as f:
                self.wfile.write(f.read())
        elif self.path.endswith('.js'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript')
            self.end_headers()
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

# If needed
# def _set_headers(self):
#         """Set headers to allow CORS and JSON content"""
#         self.send_response(200)
#         self.send_header('Content-Type', 'application/json')
#         self.send_header('Access-Control-Allow-Origin', '*')  # For CORS
#         self.end_headers()

#     def do_OPTIONS(self):
#         """Handle CORS preflight request"""
#         self.send_response(200)
#         self.send_header('Access-Control-Allow-Origin', '*')
#         self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
#         self.send_header('Access-Control-Allow-Headers', 'Content-Type')
#         self.end_headers()
