import time
import requests

from market import call_order, create_order
inf= float("inf")
ninf=float("-inf") 
 


# Replace with your actual server address
server_address = "http://localhost:5000/"
api_get_price = server_address+"trade_info" 
start= True
# Safety parameters (replace with appropriate values)
dip_threshold = -0.02  # Percentage dip threshold to trigger a buy order
surge_threshold = 0.05  # Percentage surge threshold to trigger a sell order
minimum_order_amount = 10  # Minimum quantity for an order

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
def analyze_and_trade():
    """
    Continuously retrieves the current price, analyzes for dips and surges,
    and creates orders if conditions are met.
    """

    previous_price = None

    while True and start:
        current_price = get_current_price()
        print(current_price)
        if current_price is not inf:
            if previous_price is not None:
                # Calculate price change percentage
                price_change = (current_price - previous_price) / previous_price
                print("price_change",price_change)
                if price_change <= dip_threshold and price_change < 0:  # Dip condition
                    # Create a buy order at a slightly lower price (optional)
                    order_price = current_price * (1 + dip_threshold / 2)
                    print("buy",order_price)
                    order_data = create_order(order_type="sell", price=order_price, quantity=minimum_order_amount)
                    if order_data:
                        call_order(order_data)

                elif price_change >= surge_threshold and price_change > 0:  # Surge condition
                    # Create a sell order
                    print("sell",current_price)

                    order_data = create_order(order_type="buy", price=current_price, quantity=minimum_order_amount)
                    if order_data:
                        call_order(order_data)

            previous_price = current_price

        # Implement a sleep or delay between price checks to avoid overwhelming the API
        # (replace with appropriate delay time in seconds)
        time.sleep(1)
 
if __name__ == "__main__":
    
     
    analyze_and_trade()
