import time
from func import reset
from sim_market import make_market
from stats import calculate_trade_stats,get_deals,get_current_price


import csv

def append_dict_to_csv(data, filename):
  """Appends a dictionary to a CSV file.

  Args:
      data: The dictionary to append.
      filename: The name of the existing CSV file.
  """

  # Get the keys (field names) from the dictionary (assuming they exist in the CSV)
  fieldnames = data.keys()

  with open(filename, 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Skip writing the header row if the file already exists
    writer.writerow(data)

 



if __name__ == "__main__":
    reset()
    make_market("test.csv")
    time.sleep(1)
    previous_price=None
    while True:
            try:
                current_price =  get_current_price()
                print(f"Current Price: {current_price}")

                if current_price is not None and current_price not in (float('inf'), float('-inf')):
                    if previous_price is not None:
                        if current_price==previous_price:
                          break     
                       
                previous_price = current_price
                  
            except KeyboardInterrupt:
                print("Stopping the analysis...")
                break
    # Example usage (assuming you have your transaction data in a list named 'deals')
    stats = calculate_trade_stats( get_deals("mo"))
    append_dict_to_csv(stats, "stock_summary.csv")

    print(stats)
