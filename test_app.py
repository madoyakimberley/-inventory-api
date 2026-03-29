import unittest
from main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Inventory API Running", res.json["message"])

    def test_create_item(self):
        res = self.client.post("/items", json={"name": "Test", "price": 10, "quantity": 5})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json["name"], "Test")

if __name__ == "__main__":
    unittest.main()