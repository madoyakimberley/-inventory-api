from flask import Flask, request, jsonify
from service import InventoryService

app = Flask(__name__)
service = InventoryService()

@app.route("/")
def home():
    return {"message": "Inventory API Running"}

# Create item
@app.route("/items", methods=["POST"])
def create_item():
    data = request.json
    return jsonify(service.add_item(data)), 201

# Get all items
@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(service.get_items())

# Get one item
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = service.get_item(item_id)
    return jsonify(item) if item else ({"error": "Not found"}, 404)

# Update item
@app.route("/items/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.json
    item = service.update_item(item_id, data)
    return jsonify(item) if item else ({"error": "Not found"}, 404)

# Delete item
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    return {"message": "Deleted"} if service.delete_item(item_id) else ({"error": "Not found"}, 404)

# External API search
@app.route("/external/<query>", methods=["GET"])
def external(query):
    product = service.fetch_product(query)
    return jsonify(product or {"error": "Product not found"}), 200

if __name__ == "__main__":
    app.run(debug=True)