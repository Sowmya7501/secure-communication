from flask import Flask, request, jsonify
import requests
import logging
import urllib3

# Enable detailed logging for SSL/TLS
logging.basicConfig(level=logging.DEBUG)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Enable requests debug logging
logging.getLogger("urllib3").setLevel(logging.DEBUG)
logging.getLogger("requests").setLevel(logging.DEBUG)

app = Flask(__name__)

INVENTORY_SERVICE_URL = 'https://inventory-service.services.svc.cluster.local'

@app.route('/place-order', methods=['POST'])
def place_order():
    app.logger.info("=== Starting order processing ===")
    order_data = request.json
    item_id = order_data['item_id']
    quantity = order_data['quantity']
    
    app.logger.info(f"Order request: item_id={item_id}, quantity={quantity}")

    # Check stock
    app.logger.info(f"Making SSL request to inventory service: {INVENTORY_SERVICE_URL}")
    try:
        stock_response = requests.get(f'{INVENTORY_SERVICE_URL}/check-stock/{item_id}', 
                                    verify='/var/lib/ssl/trust/ca-trust-bundle.pem')
        app.logger.info(f"Stock check response status: {stock_response.status_code}")
        app.logger.info(f"Stock check response headers: {dict(stock_response.headers)}")
        
        stock_data = stock_response.json()
        app.logger.info(f"Stock data received: {stock_data}")
    except Exception as e:
        app.logger.error(f"SSL connection error during stock check: {e}")
        return jsonify({'error': 'Failed to check stock'}), 500

    if stock_data['stock'] < quantity:
        app.logger.warning(f"Insufficient stock: available={stock_data['stock']}, requested={quantity}")
        return jsonify({'error': 'Not enough stock available'}), 400

    # Update stock
    app.logger.info(f"Making SSL request to update inventory: {INVENTORY_SERVICE_URL}")
    try:
        update_response = requests.post(f'{INVENTORY_SERVICE_URL}/update-stock', json={
            'item_id': item_id,
            'quantity': quantity
        }, verify='/var/lib/ssl/trust/ca-trust-bundle.pem')
        
        app.logger.info(f"Stock update response status: {update_response.status_code}")
        app.logger.info(f"Stock update response headers: {dict(update_response.headers)}")
        
    except Exception as e:
        app.logger.error(f"SSL connection error during stock update: {e}")
        return jsonify({'error': 'Failed to update stock'}), 500

    if update_response.status_code == 200:
        app.logger.info("Order completed successfully!")
        return jsonify({'message': 'Order placed successfully!'})
    else:
        app.logger.error(f"Stock update failed with status: {update_response.status_code}")
        return jsonify({'error': 'Failed to update stock'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, 
            ssl_context=('/var/lib/ssl/server/tls.crt', '/var/lib/ssl/server/tls.key'))
