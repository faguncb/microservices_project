# Simple Product Microservice

This project is a beginner-friendly example of a microservice built in Python. It uses only standard libraries (`http.server` and `json`) and has no external framework dependencies.

The service provides a basic API to retrieve product information.

---

## Features

-   List all available products.
-   Retrieve a single product by its ID.
-   Create new products (`POST /products`).
-   Update products fully (`PUT /products/{id}`) or partially (`PATCH /products/{id}`).
-   Delete products (`DELETE /products/{id}`).
-   In-memory data store (no database required).
-   Includes a growing suite of unit tests.
-   **Data separation**: Product data stored in external `products_data.json` file for easy management.

---

## Getting Started

### Prerequisites

-   Python 3.6+
-   `pip` for installing packages

### Installation

1.  Clone this repository to your local machine.
2.  Install the `requests` library, which is needed for running tests:
    ```bash
    pip install requests
    ```

### Project Structure

-   `product_service.py` - Main microservice code
-   `products_data.json` - **Product data file** (separated from code)
-   `test_product_service.py` - Unit tests
-   `.gitignore` - Git ignore rules
-   `.cursorignore` - Cursor AI ignore rules
-   `CURSOR_GUIDE.md` - **Guide for using Cursor AI safely and preventing unwanted commits**

---

## Usage

1.  Navigate to the project directory in your terminal.
2.  Start the microservice with the following command:
    ```bash
    python product_service.py
    ```
3.  The service will be running at `http://localhost:8000`.

---

## Running the Tests

To validate that the service is working correctly, you can run the included tests.

1.  Make sure the service is running in one terminal.
2.  Open a **second terminal** in the same project directory.
3.  Run the test suite:
    ```bash
    python -m unittest test_product_service.py
    ```

Inline notes for running tests concurrently with the server
- Option A (two terminals):
  - Terminal 1: start the server
    ```bash
    python product_service.py
    ```
  - Terminal 2: run tests
    ```bash
    python -m unittest test_product_service.py
    ```
- Option B (single terminal, background server):
  - Start the server in the background, then run tests
    ```bash
    python product_service.py &
    sleep 1 && python -m unittest test_product_service.py
    ```
  - Stop the background server on macOS/Linux
    ```bash
    lsof -ti tcp:8000 | xargs -r kill -9
    ```


---

## API Endpoints

The service exposes the following HTTP GET endpoints:

| Method | Endpoint              | Description                                 | Example Request Body                     | Example Response                                      |
|--------|-----------------------|---------------------------------------------|------------------------------------------|-------------------------------------------------------|
| `GET`  | `/products`           | Retrieves a list of all products            |                                          | `[ {"name": "Laptop", "price": 1200}, ... ]`        |
| `GET`  | `/products/{id}`      | Retrieves a single product by ID            |                                          | `{ "name": "Laptop", "price": 1200 }`              |
| `POST` | `/products`           | Creates a new product                       | `{ "name": "Headphones", "price": 199 }` | `201 Created` → `{ "id": "4", "name": "Headphones", "price": 199 }` |
| `PUT`  | `/products/{id}`      | Fully updates an existing product           | `{ "name": "New Name", "price": 123 }`  | `200 OK` → `{ "id": "4", "name": "New Name", "price": 123 }`        |
| `PATCH`| `/products/{id}`      | Partially updates an existing product       | `{ "price": 149 }`                      | `200 OK` → `{ "id": "4", "name": "...", "price": 149 }`            |
| `DELETE`| `/products/{id}`     | Deletes a product                           |                                          | `200 OK` → `{ "id": "4", "name": "...", "price": ... }`             |
| `GET`  | `/products/{non-existent-id}` | Returns a 404 error                 |                                          | `{ "error": "Product not found" }`                    |

Notes
- `POST` requires both `name` (non-empty string) and `price` (non-negative number).
- `PUT` requires both `name` and `price`.
- `PATCH` accepts either field; provided fields are validated.
- All responses are JSON.

### Curl Examples

List products
```bash
curl -s http://localhost:8000/products | jq
```

Get one product
```bash
curl -s http://localhost:8000/products/1 | jq
```

Create a product
```bash
curl -s -X POST http://localhost:8000/products \
  -H 'Content-Type: application/json' \
  -d '{"name":"Headphones","price":199}' | jq
```

Full update (PUT)
```bash
curl -s -X PUT http://localhost:8000/products/4 \
  -H 'Content-Type: application/json' \
  -d '{"name":"Headphones Pro","price":249}' | jq
```

Partial update (PATCH)
```bash
curl -s -X PATCH http://localhost:8000/products/4 \
  -H 'Content-Type: application/json' \
  -d '{"price":219}' | jq
```

Delete
```bash
curl -s -X DELETE http://localhost:8000/products/4 | jq
```

---

## Data Management

Product data is now stored in a separate `products_data.json` file. This separation provides several benefits:

-   **Easy data management**: Update product data without touching code
-   **Better organization**: Clear separation of concerns
-   **Version control**: Can track data changes separately from code changes

### Editing Product Data

To modify the initial product list, edit `products_data.json`:

```json
{
    "1": {"name": "Laptop", "price": 1200},
    "2": {"name": "Mouse", "price": 25},
    "3": {"name": "Keyboard", "price": 75}
}
```

**Note**: The service loads data on startup. Restart the service after modifying `products_data.json`.

---

## Cursor AI and Git Integration

### Preventing Unwanted Commits

**📖 For detailed guidance, see [CURSOR_GUIDE.md](CURSOR_GUIDE.md)**

This project includes:

1.  **`.gitignore`** - Prevents Python cache files, virtual environments, and IDE files from being committed
2.  **`.cursorignore`** - Tells Cursor AI to ignore certain files during analysis
3.  **`CURSOR_GUIDE.md`** - Comprehensive guide for using Cursor AI safely

### Quick Best Practices

To prevent Cursor AI from automatically committing code:

1.  **Review changes before committing**: Always review the diff manually
2.  **Use manual git commands**: Instead of relying on AI, use:
    ```bash
    git status
    git add <specific-files>
    git commit -m "Your message"
    git push
    ```
3.  **Cursor Settings**: In Cursor, go to Settings → Features → disable "Auto-commit" if enabled
4.  **Use `.cursorignore`**: Add patterns for files you don't want Cursor to modify or analyze

### Git Workflow

```bash
# Check what's changed
git status

# Add specific files only
git add product_service.py
git add products_data.json

# Commit with a meaningful message
git commit -m "Separate product data into JSON file"

# Push to remote
git push origin main
```