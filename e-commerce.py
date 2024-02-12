from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
products = []

orders = []
carts = {}

last_product_id = 0
last_orders_id = 0
# Products Routes
@app.route('/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    in_stock = request.args.get('in_stock')

    filtered_products = products.copy()

    if category:
        filtered_products = [product for product in filtered_products if product['category'] == category]

    if in_stock is not None:
        in_stock_bool = in_stock.lower() == 'true'
        filtered_products = [product for product in filtered_products if product['in_stock'] == in_stock_bool]

    return jsonify(filtered_products)

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = next((product for product in products if product['id'] == id), None)
    if product:
        return jsonify(product)
    else:
        return jsonify({'message': 'Product not found'}), 404

@app.route('/products', methods=['POST'])
def add_product():
    global last_product_id
    data = request.json
    last_product_id += 1
    data['id'] = last_product_id
    products.append(data)
    return jsonify(data), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = next((product for product in products if product['id'] == id), None)
    if product:
        data = request.json
        product.update(data)
        return jsonify(product)
    else:
        return jsonify({'message': 'Product not found'}), 404

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    global products
    products = [product for product in products if product['id'] != id]
    return jsonify({'message': 'Product deleted successfully'}), 200

# Orders Routes
@app.route('/orders', methods=['POST'])
def create_order():
    global last_orders_id
    data = request.json
    last_orders_id += 1
    data['id'] = last_orders_id
    orders.append(data)
    return jsonify(data), 201

@app.route('/orders/<int:user_id>', methods=['GET'])
def get_orders(user_id):
    user_orders = [order for order in orders if order.get('user_id') == user_id]
    return jsonify(user_orders)

# Cart Routes
@app.route('/cart/<int:user_id>', methods=['POST'])
def add_to_cart(user_id):
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not carts.get(user_id):
        carts[user_id] = {}

    if product_id in carts[user_id]:
        carts[user_id][product_id] += quantity
    else:
        carts[user_id][product_id] = quantity

    return jsonify(carts[user_id]), 200

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    return jsonify(carts.get(user_id, {})), 200

@app.route('/cart/<int:user_id>/item/<int:product_id>', methods=['DELETE'])
def remove_from_cart(user_id, product_id):
    if carts.get(user_id) and product_id in carts[user_id]:
        del carts[user_id][product_id]
        return jsonify(carts[user_id]), 200
    else:
        return jsonify({'message': 'Item not found in the cart'}), 404

if __name__ == '__main__':
    app.run(debug=True)
