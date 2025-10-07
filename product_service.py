
# product_service.py

# We use 'http.server' to create a simple web server
# and 'json' to format our data to be sent over the web.
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

# Key: In-memory data store
# In real apps, this would be a real database (e.g., Postgres/Mongo).
# Load initial products data from external JSON file
def load_products():
    """Load products from the JSON data file."""
    data_file = os.path.join(os.path.dirname(__file__), 'products_data.json')
    try:
        with open(data_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {data_file} not found. Starting with empty product list.")
        return {}
    except json.JSONDecodeError:
        print(f"Warning: {data_file} contains invalid JSON. Starting with empty product list.")
        return {}

products = load_products()

# Key: HTTP request handler – maps HTTP methods to Python methods
class ProductServiceHandler(BaseHTTPRequestHandler):
    
    def _send_response(self, status_code, data):
        """Helper function to send a JSON response."""
        # Key: Central place to set status, headers, and write JSON body
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    # A request handler for GET requests.
    def do_GET(self):
        """Handles GET requests to the service."""
        print(f"Received GET request for path: {self.path}")

        # Endpoint 1: Get all products
        # Key: Simple router via path checks
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

    # A request handler for POST requests.
    def do_POST(self):
        """Handles POST requests to create a new product."""
        # Key: Create – validate input, assign new ID, return 201
        print(f"Received POST request for path: {self.path}")

        if self.path == '/products':
            try:
                content_length_header = self.headers.get('Content-Length', '0')
                content_length = int(content_length_header) if content_length_header.isdigit() else 0
                raw_body = self.rfile.read(content_length) if content_length > 0 else b''

                # Parse JSON body
                try:
                    payload = json.loads(raw_body.decode('utf-8') or '{}')
                except json.JSONDecodeError:
                    self._send_response(400, {"error": "Invalid JSON payload"})
                    return

                name = payload.get('name')
                price = payload.get('price')

                # Basic validation
                if not isinstance(name, str) or not name.strip():
                    self._send_response(400, {"error": "Field 'name' is required and must be a non-empty string"})
                    return
                if not (isinstance(price, int) or isinstance(price, float)) or price < 0:
                    self._send_response(400, {"error": "Field 'price' is required and must be a non-negative number"})
                    return

                # Generate new ID
                if products:
                    max_id = max(int(pid) for pid in products.keys())
                    new_id = str(max_id + 1)
                else:
                    new_id = '1'

                # Store the new product
                products[new_id] = {"name": name.strip(), "price": price}

                # Respond with created resource
                created = {"id": new_id, "name": products[new_id]["name"], "price": products[new_id]["price"]}
                self._send_response(201, created)
            except Exception as e:
                self._send_response(500, {"error": f"Internal server error: {e}"})
        else:
            error_message = {"error": "Endpoint not found"}
            self._send_response(404, error_message)

    def _read_json_body(self):
        # Key: Safely read and parse JSON from request body
        content_length_header = self.headers.get('Content-Length', '0')
        content_length = int(content_length_header) if content_length_header.isdigit() else 0
        raw_body = self.rfile.read(content_length) if content_length > 0 else b''
        try:
            return json.loads(raw_body.decode('utf-8') or '{}'), None
        except json.JSONDecodeError:
            return None, {"error": "Invalid JSON payload"}

    def do_PUT(self):
        """Handles PUT requests to fully update an existing product."""
        # Key: Full update – requires both name and price
        print(f"Received PUT request for path: {self.path}")
        if self.path.startswith('/products/'):
            product_id = self.path.split('/')[-1]
            if product_id not in products:
                self._send_response(404, {"error": "Product not found"})
                return

            payload, error = self._read_json_body()
            if error is not None:
                self._send_response(400, error)
                return

            name = payload.get('name')
            price = payload.get('price')

            # PUT requires both fields
            if not isinstance(name, str) or not name.strip():
                self._send_response(400, {"error": "Field 'name' is required and must be a non-empty string"})
                return
            if not (isinstance(price, int) or isinstance(price, float)) or price < 0:
                self._send_response(400, {"error": "Field 'price' is required and must be a non-negative number"})
                return

            products[product_id] = {"name": name.strip(), "price": price}
            updated = {"id": product_id, "name": products[product_id]["name"], "price": products[product_id]["price"]}
            self._send_response(200, updated)
        else:
            self._send_response(404, {"error": "Endpoint not found"})

    def do_PATCH(self):
        """Handles PATCH requests to partially update an existing product."""
        # Key: Partial update – validates only provided fields
        print(f"Received PATCH request for path: {self.path}")
        if self.path.startswith('/products/'):
            product_id = self.path.split('/')[-1]
            if product_id not in products:
                self._send_response(404, {"error": "Product not found"})
                return

            payload, error = self._read_json_body()
            if error is not None:
                self._send_response(400, error)
                return

            # Validate provided fields only
            if 'name' in payload:
                name = payload.get('name')
                if not isinstance(name, str) or not name.strip():
                    self._send_response(400, {"error": "Field 'name' is required and must be a non-empty string"})
                    return
                products[product_id]["name"] = name.strip()

            if 'price' in payload:
                price = payload.get('price')
                if not (isinstance(price, int) or isinstance(price, float)) or price < 0:
                    self._send_response(400, {"error": "Field 'price' is required and must be a non-negative number"})
                    return
                products[product_id]["price"] = price

            updated = {"id": product_id, "name": products[product_id]["name"], "price": products[product_id]["price"]}
            self._send_response(200, updated)
        else:
            self._send_response(404, {"error": "Endpoint not found"})

    def do_DELETE(self):
        """Handles DELETE requests to remove an existing product."""
        # Key: Delete – returns deleted resource or 404 if not found
        print(f"Received DELETE request for path: {self.path}")
        if self.path.startswith('/products/'):
            product_id = self.path.split('/')[-1]
            if product_id not in products:
                self._send_response(404, {"error": "Product not found"})
                return

            deleted = {"id": product_id, "name": products[product_id]["name"], "price": products[product_id]["price"]}
            del products[product_id]
            self._send_response(200, deleted)
        else:
            self._send_response(404, {"error": "Endpoint not found"})

def run(server_class=HTTPServer, handler_class=ProductServiceHandler, port=8000):
    """Starts the HTTP server."""
    # Key: Server bootstrap – binds to port and serves forever
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting Product Microservice on port {port}...")
    httpd.serve_forever()

# This is the entry point of our script.
# When you run 'python product_service.py', this part will execute.
if __name__ == '__main__':
    # Key: Entry point – run with `python product_service.py`
    run()