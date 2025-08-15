from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory inventory for simplicity
inventory = {
    'item1': 10,
    'item2': 20,
    'item3': 15,
}

@app.route('/check-stock/<item_id>', methods=['GET'])
def check_stock(item_id):
    stock = inventory.get(item_id, 0)
    return jsonify({'item_id': item_id, 'stock': stock})

@app.route('/update-stock', methods=['POST'])
def update_stock():
    data = request.json
    item_id = data['item_id']
    quantity = data['quantity']

    if item_id in inventory and inventory[item_id] >= quantity:
        inventory[item_id] -= quantity
        return jsonify({'message': 'Stock updated successfully!'})
    else:
        return jsonify({'error': 'Not enough stock available'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=('/var/lib/ssl/server/tls.crt', '/var/lib/ssl/server/tls.key'))
