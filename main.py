from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# Enable CORS for all routes. For production, consider restricting to your Mini App's domain.
CORS(app) 

# In-memory catalog (replace with a database later if needed)
catalog = [
    {"id": 1, "name": "Foreplay Flight", "description": "Brazilian Variant - HG", "price": 3000, "unit": "HG", "stock": 10},
    {"id": 2, "name": "Midnight Ride", "description": "Brazilian Variant - 1G", "price": 4000, "unit": "1G", "stock": 10},
    {"id": 3, "name": "Galactic Gangbang", "description": "Brazilian Variant - 1½G", "price": 5000, "unit": "1.5G", "stock": 10},
    {"id": 4, "name": "Local 10 Units", "description": "Local Variant - 10 Units", "price": 400, "unit": "10 Units", "stock": 50},
    {"id": 5, "name": "Local 20 Units", "description": "Local Variant - 20 Units", "price": 500, "unit": "20 Units", "stock": 50},
    {"id": 6, "name": "Local HG", "description": "Local Variant - HG", "price": 2200, "unit": "HG", "stock": 20},
    {"id": 7, "name": "Local 1G", "description": "Local Variant - 1G", "price": 3500, "unit": "1G", "stock": 20},
    {"id": 8, "name": "Local 2G", "description": "Local Variant - 2G", "price": 5000, "unit": "2G", "stock": 20},
    {"id": 9, "name": "Poppers 10ml", "description": "Others", "price": 800, "unit": "10ml", "stock": 30},
    {"id": 10, "name": "Monogatari", "description": "Others", "price": 120, "unit": "each", "stock": 100},
    {"id": 11, "name": "Siyi", "description": "Others", "price": 120, "unit": "each", "stock": 100},
    {"id": 12, "name": "Sildenafil", "description": "Others", "price": 120, "unit": "each", "stock": 100},
    {"id": 13, "name": "Doxyprep (20pcs)", "description": "Others", "price": 220, "unit": "20pcs", "stock": 50}
]

# Using a simple dictionary for orders (in-memory, data lost on restart)
orders = {}

@app.route('/catalog', methods=['GET'])
def get_catalog():
    return jsonify(catalog)

@app.route('/catalog/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((item for item in catalog if item["id"] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route('/order', methods=['POST'])
def place_order():
    data = request.json
    user_id = data.get('user_id')
    items = data.get('items')
    address = data.get('delivery_address', '')
    payment = data.get('payment_method', 'COD')

    if not items or not isinstance(items, list):
        return jsonify({"error": "Invalid order format: 'items' array is required"}), 400

    total = 0
    for item in items:
        product_id = item.get("product_id")
        quantity = item.get("quantity")
        
        if not isinstance(product_id, int) or not isinstance(quantity, int) or quantity <= 0:
            return jsonify({"error": "Invalid item format: product_id and quantity must be positive integers"}), 400

        product = next((p for p in catalog if p["id"] == product_id), None)
        if product:
            total += product["price"] * quantity
        else:
            return jsonify({"error": f"Product ID {product_id} not found"}), 400

    order_id = str(len(orders) + 1)
    orders[order_id] = {
        "order_id": order_id,
        "user_id": user_id,
        "items": items,
        "delivery_address": address,
        "payment_method": payment,
        "total": total,
        "status": "pending"
    }

    return jsonify({"order_id": order_id, "status": "pending", "total": total})

@app.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
    order = orders.get(order_id)
    if order:
        return jsonify(order)
    return jsonify({"error": "Order not found"}), 404

if __name__ == '__main__':
    # Use environment variable for port, default to 5000 for local development
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False) # debug should be False in production
