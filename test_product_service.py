
# test_product_service.py

import unittest
import requests
import json

# The base URL of our running microservice.
BASE_URL = "http://localhost:8000"

class TestProductService(unittest.TestCase):

    def test_get_all_products(self):
        """Test the /products endpoint to get all products."""
        response = requests.get(f"{BASE_URL}/products")
        
        # Check if the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check if the response is a list of 3 items
        products = response.json()
        self.assertIsInstance(products, list)
        self.assertEqual(len(products), 3)
        print("\nTest 'get_all_products' PASSED")

    def test_get_one_product_success(self):
        """Test getting a single, existing product by its ID."""
        response = requests.get(f"{BASE_URL}/products/1")
        
        # Check for status 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check if the product name is correct
        product = response.json()
        self.assertEqual(product['name'], 'Laptop')
        print("Test 'get_one_product_success' PASSED")

    def test_get_one_product_not_found(self):
        """Test getting a product that does not exist."""
        response = requests.get(f"{BASE_URL}/products/99") # 99 is a non-existent ID
        
        # Check for status 404 (Not Found)
        self.assertEqual(response.status_code, 404)
        
        # Check the error message
        error_data = response.json()
        self.assertEqual(error_data['error'], 'Product not found')
        print("Test 'get_one_product_not_found' PASSED")
        
    def test_invalid_endpoint(self):
        """Test accessing an endpoint that doesn't exist."""
        response = requests.get(f"{BASE_URL}/invalid_path")
        
        # Check for status 404 (Not Found)
        self.assertEqual(response.status_code, 404)
        print("Test 'invalid_endpoint' PASSED")

# This allows running the tests from the command line.
if __name__ == '__main__':
    unittest.main()