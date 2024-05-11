import requests
import json

# Replace with your actual API endpoint URL


# Replace with your actual server address
server_address = "http://localhost:5000/"
api_get_price = server_address+"trade_info" 
# Prepare your order data as a dictionary
def get_current_price():
    """
    Fetches the current trade price from the specified API.

    Returns:
        float: The current trade price, or None if an error occurs.
    """

    try:
        response = requests.get(api_get_price)
        if response.status_code == 200:
            data = response.json()
            return data.get('price')
        else:
            print(f"Error getting price: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None





def create_order(user="market", order_type="buy", price=100, quantity=10, condition="ROD"):
  """
  Creates a dictionary containing order data.

  Args:
      user (str): Username for the order.
      order_type (str): Order type (e.g., "buy", "sell").
      price (float): Price for the order.
      quantity (int): Number of items to buy/sell.
      condition (str, optional): Order condition (e.g., "IOC"). Defaults to "IOC".

  Returns:
      dict: Order data dictionary.
  """

  order_data = {
      "user": user,
      "order_type": order_type.lower(),  # Ensure order type is lowercase
      "price": price,
      "quantity": quantity,
      "condition": condition,
      "market":  False  #order_type.lower() != "sell"  # Assuming market order is True for buy orders, False for sell orders
  }

  return order_data

def call_order(order_data):
# Set the headers indicating JSON content
    headers = {"Content-Type": "application/json"}

    # Build the URL
    url = f"{server_address}/order"
    
    try:
        # Send the POST request with JSON data
        response = requests.post(url, json=order_data, headers=headers)

        # Check for successful response (status code 201)
        if response.status_code == 201:
            data = response.json()
            print(f"Order received successfully! Order ID: {data.get('id')}")
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


 
if __name__ == "__main__":
    
    
    order_data=create_order(order_type="sell")
    call_order(order_data)
    order_data=create_order()
    call_order(order_data)
    order_data=create_order(order_type="sell",price=110)
    call_order(order_data)
    order_data=create_order(price=110)
    call_order(order_data)
    
 
