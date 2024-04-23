from flask import Flask, request, jsonify
from flask_cors import CORS
import controller
 
app = Flask(__name__)
# Configure CORS here
cors = CORS(app)
# Sample data (you can replace this with your actual data)

cors = CORS(app, resources={
    r"/trade_info": {"origins": "http://localhost"}
})

orders = []

@app.route('/order', methods=['POST'])
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
    
    return jsonify({"price":controller.get_trade_price(),
                    "info":controller.get_quantity()}) 


if __name__ == '__main__':
    app.run(debug=True)