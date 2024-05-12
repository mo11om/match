import time
import threading
from func import call_order, create_order,get_current_price
inf= float("inf")
ninf=float("-inf") 
 


 

class TradingStrategy:
    def __init__(self, speculative_probability, minimum_order_amount, dip_threshold=-0.02, surge_threshold=0.02, minimum_reward_threshold=0.01):
         
        """
        Initializes the trading strategy with parameters.

        Args:
            speculative_probability (float): User's confidence in price predictions (0 to 1).
            minimum_order_amount (int): Minimum quantity for buy/sell orders.
            dip_threshold (float, optional): Price decrease threshold for buying. Defaults to -0.02 (2%).
            surge_threshold (float, optional): Price increase threshold for selling. Defaults to 0.02 (2%).
            minimum_reward_threshold (float, optional): Minimum potential reward for placing orders. Defaults to 0.01 (1%).
        """
        self.speculative_probability = speculative_probability
        self.minimum_order_amount = minimum_order_amount
        self.dip_threshold = dip_threshold
        self.surge_threshold = surge_threshold
        self.minimum_reward_threshold = minimum_reward_threshold
        self.previous_price = None
     

            

        # Replace these with your actual functions
        self.get_current_price = get_current_price
        self.create_order = create_order
        self.call_order = call_order

    def start(self):
        print(f"Speculative Probability: {self.speculative_probability:.2f}")
        while True:
            try:
                current_price = self.get_current_price()
                print(f"Current Price: {current_price}")

                if current_price is not None and current_price not in (float('inf'), float('-inf')):
                    if self.previous_price is not None:
                        price_change = (current_price - self.previous_price) 
                        potential_reward = abs(price_change)

                        print(f"Price Change: {price_change:}")
                        print(f"Potential Reward: {potential_reward:}")

                        self.analyze_and_trade(current_price, price_change, potential_reward)

                self.previous_price = current_price
                time.sleep(0.5)  # Adjust sleep time as needed
            except KeyboardInterrupt:
                print("Stopping the analysis...")
                break

    def analyze_and_trade(self, current_price, price_change, potential_reward):
        if   price_change > 0:
            # if potential_reward * self.speculative_probability >= self.minimum_reward_threshold:
                order_price = int(current_price +1)
                print(f"Sell Order: {order_price:}")
                # Create order in a separate thread
                order_thread = threading.Thread(target=self.create_and_call_order, args=("mo", "sell", order_price, self.minimum_order_amount))
                order_thread.start() 
                order_price = int(current_price -2 )
                print(f"Buy Order: {order_price:.2f}")
                # Create order in a separate thread
                
                order_thread = threading.Thread(target=self.create_and_call_order, args=("mo", "buy", order_price, self.minimum_order_amount))
                order_thread.start()

        # elif  price_change > 0:
        #     # if potential_reward * self.speculative_probability >= self.minimum_reward_threshold:
        #         order_price = int(current_price +1 )
        #         print(f"Buy Order: {order_price:.2f}")
        #         # Create order in a separate thread
                
        #         order_thread = threading.Thread(target=self.create_and_call_order, args=("user", "buy", order_price, self.minimum_order_amount))
        #         order_thread.start()

    def create_and_call_order(self, user, order_type, price, quantity):
        order_data = self.create_order(user=user, order_type=order_type,price= price, quantity=quantity)
        print(order_data)
        if order_data:
            self.call_order(order_data)

# Example usage (same as before)
 
 

if __name__ == "__main__":
    
        # Safety parameters (replace with appropriate values)
    dip_threshold = -0.0001  # Percentage dip threshold to trigger a buy order
    surge_threshold = 0.0001  # Percentage surge threshold to trigger a sell order
    minimum_order_amount = 10  # Minimum quantity for an order
    minimum_reward_threshold=0.00001
    strategy = TradingStrategy(1, 100,dip_threshold,surge_threshold,minimum_reward_threshold)  # Replace with your parameters
    strategy.start()
     