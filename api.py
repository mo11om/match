from flask import Flask, request, jsonify
import controller
app = Flask(__name__)

# Sample data (you can replace this with your actual data)
orders = []

@app.route('/receive_order', methods=['POST'])
def receive_order():
    """
    Receives order data in JSON format and adds it to the list of orders.
    """
    try:
        order_data = request.get_json()

        id =controller.input_order_from_json(order_data)
        print(id)
        # user = order_data.get("user")
        # order_type = order_data.get("order_type")
        # price = order_data.get("price")
        # quantity = order_data.get("quantity")
        # condition = order_data.get("condition")
        # market = order_data.get("market", False)  # Default to False if not specified
        
        # # Create an Order object (you can use your existing Order class)
        # new_order = {
        #     "user": user,
        #     "order_type": order_type,
        #     "price": price,
        #     "quantity": quantity,
        #     "condition": condition,
        #     "market": market
        # }

        # orders.append(new_order)
        return jsonify({"message": "Order received successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)