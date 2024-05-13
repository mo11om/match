import time
from sim_market import make_market
from stats import calculate_trade_stats,get_deals
if __name__ == "__main__":
   
    make_market("test.csv")
    time.sleep(1)
    # Example usage (assuming you have your transaction data in a list named 'deals')
    stats = calculate_trade_stats( get_deals("mo"))
    print(stats)
