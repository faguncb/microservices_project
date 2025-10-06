# Simple Product Microservice

This project is a beginner-friendly example of a microservice built in Python. It uses only standard libraries (`http.server` and `json`) and has no external framework dependencies.

The service provides a basic API to retrieve product information.

---

## Features

-   List all available products.
-   Retrieve a single product by its ID.
-   In-memory data store (no database required).
-   Includes a full suite of unit tests.

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

---

## API Endpoints

The service exposes the following HTTP GET endpoints:

| Method | Endpoint              | Description                      | Example Response                                    |
|--------|-----------------------|----------------------------------|-----------------------------------------------------|
| `GET`  | `/products`           | Retrieves a list of all products | `[{"name": "Laptop", "price": 1200}, ...]`          |
| `GET`  | `/products/{id}`      | Retrieves a single product by ID | `{"name": "Laptop", "price": 1200}`                 |
| `GET`  | `/products/{non-existent-id}` | Returns a 404 error          | `{"error": "Product not found"}`                |