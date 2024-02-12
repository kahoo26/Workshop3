from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from datetime import date

app = Flask(__name__)

# Configuration de la base de données MySQL
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'nextapp'

mysql = MySQL(app)

last_product_id = 0
last_orders_id = 0
# Products Routes
@app.route('/products', methods=['GET'])
def get_products():
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM product")
    product = cur.fetchall()
    return jsonify(product)

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM product WHERE id = %s", (id,))
    product = cur.fetchone()
    if product:
        return jsonify(product)
    else:
        return jsonify({'message': 'Product not found'}), 404

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    cur = mysql.get_db().cursor()
    cur.execute("INSERT INTO product (category, name, description, price) VALUES (%s, %s, %s, %s)",
                (data['category'], data['name'], data['description'], data['price']))
    mysql.get_db().commit()
    return jsonify(data), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    cur = mysql.get_db().cursor()
    cur.execute("UPDATE product SET name=%s, description=%s, price=%s, category=%s WHERE id=%s",
                (data['name'], data['description'], data['price'], data['category'], id))
    mysql.get_db().commit()
    return jsonify(data)

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    cur = mysql.get_db().cursor()
    cur.execute("DELETE FROM product WHERE id = %s", (id))
    mysql.get_db().commit()
    return jsonify({'message': 'Product deleted successfully'}), 200

# Orders Routes
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    cur = mysql.get_db().cursor()
    cur.execute("INSERT INTO orders (product_id, quantity, user_id, date) VALUES (%s, %s, %s, %s)",
                (data['product_id'], data['quantity'], data['user_id'], date.today()))
    mysql.get_db().commit()
    return jsonify(data), 201

@app.route('/orders/<int:user_id>', methods=['GET'])
def get_orders(user_id):
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM orders WHERE user_id = %s", (user_id))
    orders = cur.fetchall()
    return jsonify(orders)

# Cart Routes
@app.route('/cart/<int:user_id>', methods=['POST'])
def add_to_cart(user_id):
    data = request.json
    cur = mysql.get_db().cursor()
    cur.execute("INSERT INTO cart (product_id, quantity, user_id) VALUES (%s, %s, %s)",
                (data['product_id'], data['quantity'],user_id))
    mysql.get_db().commit()
    return jsonify(data), 200

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM cart WHERE user_id = %s", (user_id,))
    cart_items = cur.fetchall()
    return jsonify(cart_items), 200

@app.route('/cart/<int:user_id>/item/<int:product_id>', methods=['DELETE'])
def remove_from_cart(user_id, product_id):
    cur = mysql.get_db().cursor()
    cur.execute("DELETE FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
    mysql.get_db().commit()
    return jsonify({'message': 'Item removed from cart'}), 200

if __name__ == '__main__':
    app.run(debug=True)
