import requests
import json
from func import get_current_price
def get_deals(user):
    url = "http://127.0.0.1:5000/deals"

    # Define the data as a dictionary
    data = {"user": user}

    # Convert the data dictionary to JSON format
    json_data = json.dumps(data)

    # Set the headers to specify JSON content type
    headers = {'Content-type': 'application/json'}

    # Send the POST request with JSON data
    response = requests.post(url, data=json_data, headers=headers)

    # Check for successful response status code
    if response.status_code == 200:
    # Get the response data as JSON
        response_json = response.json()
        print(response_json)
        
    else:
        print("Error:", response.status_code)
    return response_json
def calculate_trade_stats(data):
  """
  Calculates average buy price, average sell price, total quantity, and profit.

  Args:
      data: A list of lists representing transactions. Each inner list contains
          information about a transaction (deal id, type, price, quantity, timestamp).

  Returns:
      A dictionary containing the calculated statistics:
          average_buy_price: The average price at which items were bought.
          average_sell_price: The average price at which items were sold.
          total_quantity: The total number of items bought and sold.
          profit: The total profit earned (positive) or loss (negative).
  """
  cur_price=get_current_price()
  total_buy_price = 0
  total_sell_price = 0
  total_buy_quantity = 0
  total_sell_quantity = 0

  for deal in data:
    print(deal)
    # Extract relevant information from each transaction
    price = deal.get("price")  # Assuming price is at index 2
    quantity = deal.get("quantity")  # Assuming quantity is at index 3

    # Accumulate buy and sell prices based on transaction type
    if deal.get("order_type") == "buy":
      total_buy_price += price * quantity
      total_buy_quantity += quantity
    else:
      total_sell_price += price * quantity
      total_sell_quantity+=quantity

    

  # Calculate average prices and profit
  average_buy_price = total_buy_price / total_buy_quantity if total_buy_quantity else 0
  average_sell_price = total_sell_price / total_sell_quantity if total_sell_quantity else 0
  remain_quantity=total_buy_quantity-total_sell_quantity
  print(total_sell_price)
  print(total_buy_price)

  profit = total_sell_price - total_buy_price  +  cur_price * remain_quantity  

  return {
    "average_buy_price": average_buy_price,
    "total_buy_quantity":total_buy_quantity,
    "total_sell_quantity":total_sell_quantity,
    "average_sell_price": average_sell_price,
    "remain_quantity": remain_quantity,
    "profit": profit,
  }


if __name__ == "__main__":
   
    # Example usage (assuming you have your transaction data in a list named 'deals')
    stats = calculate_trade_stats( get_deals("user"))
    print(stats)
