from http.server import BaseHTTPRequestHandler, HTTPServer
from main.model.figcheck import figcheck  # Ensure correct path to figcheck.py
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/get_text':
            # Read the length of the content
            content_length = int(self.headers['Content-Length'])
            # Read and decode the POST data
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # Parse the received JSON data
            try:
                data = json.loads(post_data)
                text_input = data.get('text_input', '')  # Extract the 'text_input' key

                if text_input:
                    # Call the figcheck function to process the input text
                    result = figcheck(text_input)
                    
                    # Send back the JSON result
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(result).encode('utf-8'))
                else:
                    # If no text_input was provided, return an error
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "No text_input provided"}).encode('utf-8'))

            except json.JSONDecodeError:
                # If the JSON data can't be decoded, send an error response
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode('utf-8'))

    def do_GET(self):
        # Serve your HTML/CSS/JS files
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
        #pass

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
