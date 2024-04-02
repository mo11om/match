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
        
         
        # controller.show_deal()
        
        return jsonify({"message": "Order received successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/deals", methods=['POST'])
def get_orders_by_user():
    """
    Get order from names
    """
    data=request.get_json()
    user = data.get("user")
    return jsonify(controller.get_deal(user)) 

@app.route("/trade_info", methods=['GET'])
def get_trade_info():
    """
    Get order from names
    """
    
    return jsonify({"price":controller.get_trade_price()}) 


if __name__ == '__main__':
    app.run(debug=True)