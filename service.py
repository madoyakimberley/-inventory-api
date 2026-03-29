import requests

class InventoryService:
    def __init__(self):
        self.items = []
        self.current_id = 1

    # CRUD Operations
    def add_item(self, data):
        item = {
            "id": self.current_id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": data.get("quantity")
        }
        self.items.append(item)
        self.current_id += 1
        return item

    def get_items(self):
        return self.items

    def get_item(self, item_id):
        return next((i for i in self.items if i["id"] == item_id), None)

    def update_item(self, item_id, data):
        item = self.get_item(item_id)
        if item:
            item.update(data)
            return item

    def delete_item(self, item_id):
        item = self.get_item(item_id)
        if item:
            self.items.remove(item)
            return True
        return False

    # Open Food Facts API
    def fetch_product(self, query):
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        params = {
            "search_terms": query,
            "search_simple": 1,
            "action": "process",
            "json": 1
        }
        headers = {
            "User-Agent": "InventoryCLI/1.0 (kimberley@example.com)"
        }

        try:
            res = requests.get(url, params=params, headers=headers, timeout=5)
            res.raise_for_status()
            data = res.json()

            if data.get("products"):
                p = data["products"][0]
                return {
                    "name": p.get("product_name", "Unknown"),
                    "brand": p.get("brands", "Unknown"),
                    "ingredients": p.get("ingredients_text", "N/A")
                }
            return None
        except:
            return None

    # Add OpenFoodFacts product to local inventory
    def add_external_item(self, product):
        item = {
            "id": self.current_id,
            "name": product.get("name", "Unknown"),
            "price": 0,  # Default price; user can update manually
            "quantity": 1,
            "brand": product.get("brand", "")
        }
        self.items.append(item)
        self.current_id += 1
        return item