
# product_service.py

# We use 'http.server' to create a simple web server
# and 'json' to format our data to be sent over the web.
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# This is our in-memory "database" of products.
# In a real application, this would come from a database like PostgreSQL or MongoDB.
products = {
    "1": {"name": "Laptop", "price": 1200},
    "2": {"name": "Mouse", "price": 25},
    "3": {"name": "Keyboard", "price": 75},
}

# This class will handle all incoming requests to our server.
class ProductServiceHandler(BaseHTTPRequestHandler):
    
    def _send_response(self, status_code, data):
        """Helper function to send a JSON response."""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    # A request handler for GET requests.
    def do_GET(self):
        """Handles GET requests to the service."""
        print(f"Received GET request for path: {self.path}")

        # Endpoint 1: Get all products
        # If the path is '/products', return the whole list.
        if self.path == '/products':
            self._send_response(200, list(products.values()))
            
        # Endpoint 2: Get a single product by ID
        # If the path looks like '/products/1', '/products/2', etc.
        elif self.path.startswith('/products/'):
            # Extract the ID from the path.
            try:
                product_id = self.path.split('/')[-1]
                
                # Check if the product exists in our "database".
                if product_id in products:
                    self._send_response(200, products[product_id])
                else:
                    # If not found, send a 404 error.
                    error_message = {"error": "Product not found"}
                    self._send_response(404, error_message)
            except Exception as e:
                error_message = {"error": f"Invalid request: {e}"}
                self._send_response(400, error_message)
        
        # If the path is not recognized, send a 404 error.
        else:
            error_message = {"error": "Endpoint not found"}
            self._send_response(404, error_message)

def run(server_class=HTTPServer, handler_class=ProductServiceHandler, port=8000):
    """Starts the HTTP server."""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting Product Microservice on port {port}...")
    httpd.serve_forever()

# This is the entry point of our script.
# When you run 'python product_service.py', this part will execute.
if __name__ == '__main__':
    run()