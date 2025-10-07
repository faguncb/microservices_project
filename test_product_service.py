
# test_product_service.py
# Key: This file uses Python's built-in unittest to exercise the HTTP API.
# Tests make real HTTP requests to the running service using the 'requests' library.

import unittest
import requests
import json

# Key: Base URL for all requests; the service must be running on this port.
BASE_URL = "http://localhost:8000"

class TestProductService(unittest.TestCase):
    # Key: Each method whose name starts with 'test_' is an independent test case.
    # They assert on HTTP status codes and JSON response bodies.

    def test_get_all_products(self):
        # Key: Smoke test for the collection endpoint
        """Test the /products endpoint to get all products."""
        response = requests.get(f"{BASE_URL}/products")
        
        # Check if the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check if the response is a list with at least the original 3 items
        products = response.json()
        self.assertIsInstance(products, list)
        self.assertGreaterEqual(len(products), 3)
        print("\nTest 'get_all_products' PASSED")

    def test_get_one_product_success(self):
        # Key: Fetch a known product by ID
        """Test getting a single, existing product by its ID."""
        response = requests.get(f"{BASE_URL}/products/1")
        
        # Check for status 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check if the product name is correct
        product = response.json()
        self.assertEqual(product['name'], 'Laptop')
        print("Test 'get_one_product_success' PASSED")

    def test_get_one_product_not_found(self):
        # Key: Not-found path should return 404 with error JSON
        """Test getting a product that does not exist."""
        response = requests.get(f"{BASE_URL}/products/99") # 99 is a non-existent ID
        
        # Check for status 404 (Not Found)
        self.assertEqual(response.status_code, 404)
        
        # Check the error message
        error_data = response.json()
        self.assertEqual(error_data['error'], 'Product not found')
        print("Test 'get_one_product_not_found' PASSED")
        
    def test_invalid_endpoint(self):
        # Key: Unknown route should return 404
        """Test accessing an endpoint that doesn't exist."""
        response = requests.get(f"{BASE_URL}/invalid_path")
        
        # Check for status 404 (Not Found)
        self.assertEqual(response.status_code, 404)
        print("Test 'invalid_endpoint' PASSED")

    def test_create_product(self):
        # Key: Happy-path creation returns 201 and echoes fields with a new id
        """Test creating a new product using POST /products."""
        new_product = {"name": "Headphones", "price": 199}
        response = requests.post(f"{BASE_URL}/products", json=new_product)

        # Expect 201 Created
        self.assertEqual(response.status_code, 201)

        created = response.json()
        self.assertIn('id', created)
        self.assertEqual(created['name'], new_product['name'])
        self.assertEqual(created['price'], new_product['price'])
        print("Test 'create_product' PASSED")

    def test_create_product_invalid_json(self):
        # Key: Malformed JSON should be rejected with 400 and clear error
        """POST /products with invalid JSON should return 400."""
        response = requests.post(
            f"{BASE_URL}/products",
            data="{invalid json}",
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), 'Invalid JSON payload')
        print("Test 'create_product_invalid_json' PASSED")

    def test_create_product_missing_name(self):
        # Key: Validation - 'name' is required and must be non-empty
        """POST /products without name should return 400."""
        payload = {"price": 10}
        response = requests.post(f"{BASE_URL}/products", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json().get('error'),
            "Field 'name' is required and must be a non-empty string"
        )
        print("Test 'create_product_missing_name' PASSED")

    def test_create_product_empty_name(self):
        # Key: Validation - whitespace-only name is not allowed
        """POST /products with empty name should return 400."""
        payload = {"name": "   ", "price": 10}
        response = requests.post(f"{BASE_URL}/products", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json().get('error'),
            "Field 'name' is required and must be a non-empty string"
        )
        print("Test 'create_product_empty_name' PASSED")

    def test_create_product_missing_price(self):
        # Key: Validation - 'price' is required
        """POST /products without price should return 400."""
        payload = {"name": "Item"}
        response = requests.post(f"{BASE_URL}/products", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json().get('error'),
            "Field 'price' is required and must be a non-negative number"
        )
        print("Test 'create_product_missing_price' PASSED")

    def test_create_product_non_numeric_price(self):
        # Key: Validation - 'price' must be numeric
        """POST /products with non-numeric price should return 400."""
        payload = {"name": "Item", "price": "free"}
        response = requests.post(f"{BASE_URL}/products", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json().get('error'),
            "Field 'price' is required and must be a non-negative number"
        )
        print("Test 'create_product_non_numeric_price' PASSED")

    def test_create_product_negative_price(self):
        # Key: Validation - 'price' cannot be negative
        """POST /products with negative price should return 400."""
        payload = {"name": "Item", "price": -1}
        response = requests.post(f"{BASE_URL}/products", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json().get('error'),
            "Field 'price' is required and must be a non-negative number"
        )
        print("Test 'create_product_negative_price' PASSED")

    def test_put_update_product(self):
        # Key: PUT is a full replacement; requires both fields
        """Create a product, then fully update it via PUT."""
        create_resp = requests.post(f"{BASE_URL}/products", json={"name": "Temp", "price": 10})
        self.assertEqual(create_resp.status_code, 201)
        product_id = create_resp.json()["id"]

        put_resp = requests.put(f"{BASE_URL}/products/{product_id}", json={"name": "Updated", "price": 20})
        self.assertEqual(put_resp.status_code, 200)
        body = put_resp.json()
        self.assertEqual(body["id"], product_id)
        self.assertEqual(body["name"], "Updated")
        self.assertEqual(body["price"], 20)
        print("Test 'put_update_product' PASSED")

    def test_put_missing_fields(self):
        # Key: PUT without one of the required fields should be 400
        """PUT requires both name and price."""
        create_resp = requests.post(f"{BASE_URL}/products", json={"name": "Temp2", "price": 15})
        self.assertEqual(create_resp.status_code, 201)
        product_id = create_resp.json()["id"]

        resp1 = requests.put(f"{BASE_URL}/products/{product_id}", json={"name": "OnlyName"})
        self.assertEqual(resp1.status_code, 400)
        resp2 = requests.put(f"{BASE_URL}/products/{product_id}", json={"price": 999})
        self.assertEqual(resp2.status_code, 400)
        print("Test 'put_missing_fields' PASSED")

    def test_patch_partial_update(self):
        # Key: PATCH can update one field at a time
        """PATCH should allow updating only one field at a time."""
        create_resp = requests.post(f"{BASE_URL}/products", json={"name": "Patchable", "price": 30})
        self.assertEqual(create_resp.status_code, 201)
        product_id = create_resp.json()["id"]

        patch_resp = requests.patch(f"{BASE_URL}/products/{product_id}", json={"price": 35})
        self.assertEqual(patch_resp.status_code, 200)
        self.assertEqual(patch_resp.json()["price"], 35)

        patch_resp2 = requests.patch(f"{BASE_URL}/products/{product_id}", json={"name": "Patched"})
        self.assertEqual(patch_resp2.status_code, 200)
        self.assertEqual(patch_resp2.json()["name"], "Patched")
        print("Test 'patch_partial_update' PASSED")

    def test_patch_validation(self):
        # Key: PATCH still validates any provided fields
        """PATCH validation for name/price values."""
        create_resp = requests.post(f"{BASE_URL}/products", json={"name": "Patchable2", "price": 40})
        self.assertEqual(create_resp.status_code, 201)
        product_id = create_resp.json()["id"]

        resp1 = requests.patch(f"{BASE_URL}/products/{product_id}", json={"name": "   "})
        self.assertEqual(resp1.status_code, 400)
        resp2 = requests.patch(f"{BASE_URL}/products/{product_id}", json={"price": -5})
        self.assertEqual(resp2.status_code, 400)
        resp3 = requests.patch(f"{BASE_URL}/products/{product_id}", json={"price": "free"})
        self.assertEqual(resp3.status_code, 400)
        print("Test 'patch_validation' PASSED")

    def test_delete_product_success(self):
        # Key: DELETE returns the deleted resource; subsequent GET is 404
        """Create a product, delete it, and verify it is gone."""
        create_resp = requests.post(f"{BASE_URL}/products", json={"name": "ToDelete", "price": 5})
        self.assertEqual(create_resp.status_code, 201)
        product_id = create_resp.json()["id"]

        delete_resp = requests.delete(f"{BASE_URL}/products/{product_id}")
        self.assertEqual(delete_resp.status_code, 200)
        body = delete_resp.json()
        self.assertEqual(body["id"], product_id)

        # Subsequent GET should be 404
        get_resp = requests.get(f"{BASE_URL}/products/{product_id}")
        self.assertEqual(get_resp.status_code, 404)
        print("Test 'delete_product_success' PASSED")

    def test_delete_product_not_found(self):
        # Key: Deleting a missing product yields 404 with error JSON
        """Deleting a non-existent product returns 404."""
        delete_resp = requests.delete(f"{BASE_URL}/products/999999")
        self.assertEqual(delete_resp.status_code, 404)
        self.assertEqual(delete_resp.json().get('error'), 'Product not found')
        print("Test 'delete_product_not_found' PASSED")

# This allows running the tests from the command line.
if __name__ == '__main__':
    unittest.main()