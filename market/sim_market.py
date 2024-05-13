import pandas as pd
import threading
import time
from func import create_order,call_order 
def read_large_csv(filename, chunksize=10000):
  """
  Reads a large CSV file in chunks.

  Args:
    filename: The name of the CSV file.
    chunksize: The number of rows to read at a time.

  Yields:
    A pandas DataFrame for each chunk of the CSV file.
  """
  for chunk in pd.read_csv(filename, chunksize=chunksize):
    yield chunk

 
def read_csv_data(filename):
  """
  Reads CSV data into a pandas DataFrame.

  Args:
      filename (str): The name of the CSV file.

  Returns:
      pandas.DataFrame: The DataFrame containing the CSV data.
  """
  data = pd.read_csv(filename)
  return data

def create_orders_from_data(data):
  """
  Creates order dictionaries from CSV data and potentially calls them.

  Args:
      data (pandas.DataFrame): The DataFrame containing CSV data.
      
  """
  previous_time=0
  order_by_price={}
  for index, row in data.iterrows():
    # Extract relevant data from each row (assuming time is irrelevant)
        # Extract time
    current_time = int(row[0])

    # Check if new time encountered
    if current_time != previous_time:
      print(order_by_price)
      previous_time=current_time
      iter_order_threaded(orders_by_price=order_by_price)
      order_by_price={} 
    price = int(row[1])
    quantity = int(row[2])
    update_orders(orders_by_price=order_by_price,price=price,quantity=quantity)
      
def update_orders(orders_by_price, price:int, quantity:int):
  """
  Updates the orders_by_price dictionary with a new order or updates an existing one.

  Args:
      orders_by_price (dict): The dictionary containing orders grouped by price.
      price (int): The price of the order.
      quantity (int): The quantity of the order.
  """
  # Check if key (price) exists
  if price in orders_by_price:
    # Update quantity for existing order
    orders_by_price[price]+= quantity
    # orders_by_price[price]["quantity"] += quantity
  else:
    # Add new order for the price
    orders_by_price[price] = quantity#{"price": price, "quantity": quantity}

 
def iter_order(orders_by_price:dict):
  # Create order data dictionary
  for price,quantity in orders_by_price.items():
    order_data = create_order(user="market",order_type="buy", price=price, quantity=quantity)
    print(f"Order data created: {order_data}")  # Print order data for review

    if order_data :
      call_order(order_data)
    # Optionally call the order (uncomment to enable)
    # call_order(order_data, server_address)    

def iter_order_threaded(orders_by_price: dict):
    # threads = []
    time.sleep(0.02)

    for price, quantity in orders_by_price.items():
        order_data = create_order(user="market",order_type="buy", price=price, quantity=quantity)
        print(f"Order data created: {order_data}")

        # Create and start a thread for each order
        thread = threading.Thread(target=call_order, args=(order_data,))
        thread.start()
        # threads.append(thread)


    # for thread in threads:
    #     thread.join()

    for price, quantity in orders_by_price.items():
    
        order_data = create_order(user="market",order_type="sell", price=price, quantity=quantity)  # Use absolute value for sell quantity
        thread = threading.Thread(target=call_order, args=(order_data,))
        thread.start()
        # threads.append(thread)


    # # Wait for all threads to finish
    # for thread in threads:
    #     thread.join()

# Example usage


def make_market(filename:str):
  data = read_csv_data(filename) 

  create_orders_from_data(data)
  


if __name__ == "__main__":
  #  for chunk in read_large_csv("market.csv"):
  #       # Process the chunk of data
  #       print(chunk) 
  filename = "test.csv"
  data = read_csv_data(filename) 

  create_orders_from_data(data)
  