from sortedcontainers import SortedDict
from enum import Enum
from time import time

inf= float("inf")
ninf=float("-inf")
class Condition(Enum):
    FOK = 1  # Fill or Kill
    IOC = 2  # Immediate or Cancel
    ROD = 3  # Regular Order


class Order:
    order_counter = 0  # A class variable to assign unique order IDs

    def __init__(self, order_type, price, quantity, condition,market=False)->int:
    
        Order.order_counter += 1
        self.order_id = Order.order_counter  # Unique order ID
        self.order_type = order_type  # 'buy' or 'sell'
        self.price = price
        self.quantity = quantity
        self.timestamp = int(time())  # Current timestamp
        self.condition = condition
        self.market= market

    def get_order_id(self):
        return self.order_id
    def __repr__(self):
        return f"Order(order_id={self.order_id}, order_type='{self.order_type}', price={self.price}, quantity={self.quantity}, timestamp={self.timestamp}, condition={self.condition})"


class OrderBook:
    def __init__(self):
        self.buy_order_book = SortedDict()
        self.buy_Cumulative_quantity=SortedDict()
        self.sell_order_book = SortedDict()
        self.sell_Cumulative_quantity=SortedDict()
    def check_fill_or_kill(self ,order:Order )->bool:
        Cumulative_quantity=0
        if order.order_type=="buy":
            matching_prices = self.sell_Cumulative_quantity.irange(maximum=order.price )  # Get prices less than or equal to buy order price
           
            for price in matching_prices:
                     
                    Cumulative_quantity += self.sell_Cumulative_quantity [ price]
        elif order.order_type=="sell":
            matching_prices =self.buy_order_book.irange(minimum=order.price, reverse=True)  # Get prices less than or equal to buy order price
            print (" matching_prices" ) 
            for price in matching_prices:
                    print ("price in matching_prices",price) 
                    Cumulative_quantity += self.buy_Cumulative_quantity [ price]
                    print(Cumulative_quantity)
        if Cumulative_quantity>= order.quantity :
            return True
        else :
            return False
    def update_Cumulative_quantity(self,order:Order,add=True,partial=False,partnum:int=0 ):  
        if order.order_type=="buy":
            if add:
                if order.price not in self.buy_Cumulative_quantity:
                    self.buy_Cumulative_quantity[order.price] =  order. quantity
                else:
                    self.buy_Cumulative_quantity[order.price]+=order.quantity
            else :
               
                if partial:
                    self.buy_Cumulative_quantity[order.price]-=partnum
                else:
                    self.buy_Cumulative_quantity[order.price]-=order.quantity
                 
                
                 
        if order.order_type=="sell":
            if add:
                if order.price not in self.sell_Cumulative_quantity:
                                self.sell_Cumulative_quantity[order.price] =  order. quantity
                else:
                    self.sell_Cumulative_quantity[order.price]+=order.quantity
            else :
                if partial:
                    self.sell_Cumulative_quantity[order.price]-=partnum
                else:
                    self.sell_Cumulative_quantity[order.price]-=order.quantity
    def process_order(self, order:Order):
         
        if order.order_type == 'buy':
            # Look for matching sell orders
            matching_prices = self.sell_order_book.irange(maximum=order.price,  )  # Get prices less than or equal to buy order price
             
            if order.condition == Condition.FOK:
                # FOK (Fill or Kill) order should execute fully or not at all
                
                if (self.check_fill_or_kill(order)):
                    for price in matching_prices:
                        
                        if order.quantity == 0:
                            break
                        
                        matching_orders = self.sell_order_book[price]
                        for sell_order in matching_orders:
                            if order.quantity == 0:
                                break

                            if sell_order.quantity <= order.quantity:
                                # Full match
                                print(f"Trade executed {order.condition}: {sell_order.quantity} at price {sell_order.price} seller_id {sell_order.order_id}  to buyer order_id={order.order_id}")
                                order.quantity -= sell_order.quantity
                                self.update_Cumulative_quantity( matching_orders.pop(0),False)  # Remove the first order in the list
                            else:
                                # Partial match
                                print(f"Trade executed {order.condition}: {order.quantity} at price {sell_order.price} seller_id {sell_order.order_id}  to buyer  to order_id={order.order_id}")
                                sell_order.quantity -= order.quantity
                                
                                self.update_Cumulative_quantity( sell_order,add=False,partial= True, partnum= order.quantity)
                                order.quantity = 0
                                return  # Cancel remaining IOC order
                else:
                    print(f"FOK order canceled: order_id={order.order_id}")
                    return    

            elif order.condition == Condition.IOC:
                # IOC (Immediate or Cancel) order should execute as much as possible and cancel the rest

                for price in matching_prices:
                  
                    if order.quantity == 0:
                        break
                      
                    matching_orders = self.sell_order_book[price]
                    for sell_order in matching_orders:
                        if order.quantity == 0:
                            break

                        if sell_order.quantity <= order.quantity:
                            # Full match
                            print(f"Trade executed (IOC): {sell_order.quantity} at price {sell_order.price} seller_id {sell_order.order_id}  to buyer order_id={order.order_id}")
                            order.quantity -= sell_order.quantity
                            self.update_Cumulative_quantity( matching_orders.pop(0),False)  # Remove the first order in the list
                        else:
                            # Partial match
                            print(f"Trade executed (IOC): {order.quantity} at price {sell_order.price} seller_id {sell_order.order_id}  to buyer  to order_id={order.order_id}")
                            sell_order.quantity -= order.quantity
                             
                            self.update_Cumulative_quantity( sell_order,add=False,partial= True, partnum= order.quantity)
                            order.quantity = 0
                            return  # Cancel remaining IOC order
                    
            elif order.condition == Condition.ROD:
                # Regular Order
                for price in matching_prices:
                    if order.quantity == 0:
                        break

                    matching_orders = self.sell_order_book[price]
                    for sell_order in matching_orders:
                        if order.quantity == 0:
                            break

                        if sell_order.quantity <= order.quantity:
                            # Full match
                            print(f"Trade executed (ROD): {sell_order.quantity} at price {sell_order.price} to order_id={order.order_id}")
                            order.quantity -= sell_order.quantity
                            self.update_Cumulative_quantity( matching_orders.pop(0),False)  # Remove the first order in the list
                        else:
                            # Partial match
                            print(f"Trade executed (ROD): {order.quantity} at price {sell_order.price} to order_id={order.order_id}")
                            sell_order.quantity -= order.quantity
                            self.update_Cumulative_quantity( sell_order,add=False,partial= True, partnum= order.quantity)
                            order.quantity = 0

                if order.quantity > 0:
                    # Add remaining quantity to the buy order book
                    if order.price not in self.buy_order_book:
                        self.buy_order_book[order.price] = []
                    self.buy_order_book[order.price].append(order)
                    self.update_Cumulative_quantity(order)
                    

        elif order.order_type == 'sell':
            # Look for matching buy orders
            matching_prices = self.buy_order_book.irange(minimum=order.price, reverse=True)  # Get prices greater than or equal to sell order price

            if order.condition == Condition.FOK:
                # FOK (Fill or Kill) order should execute fully or not at all
                if (self.check_fill_or_kill(order)) :
                    #
                    for price in matching_prices:
                        if order.quantity == 0:
                            break

                        matching_orders = self.buy_order_book[price]
                        for buy_order in matching_orders:
                            if order.quantity == 0:
                                break

                            if buy_order.quantity <= order.quantity:
                                # Full match
                                print(f"Trade executed {order.condtion}: {buy_order.quantity} at price {buy_order.price} to order_id={order.order_id}")
                                order.quantity -= buy_order.quantity
                                # Remove the first order in the list
                                self.update_Cumulative_quantity( matching_orders.pop(0),False)
                            else:
                                # Partial match
                                print(f"Trade executed {order.condtion}: {order.quantity} at price {buy_order.price} to order_id={order.order_id}")
                                buy_order.quantity -= order.quantity
                            
                                order.quantity = 0
                                print("buyer cumu",self.buy_Cumulative_quantity)
                                self.update_Cumulative_quantity( buy_order,add=False,partial= True, partnum=  order.quantity)

                                return  # Cancel remaining IOC order  
                else:
                    print(f"FOK order canceled: order_id={order.order_id}")
                    return     
            elif order.condition == Condition.IOC:
                # IOC (Immediate or Cancel) order should execute as much as possible and cancel the rest
    
                for price in matching_prices:
                    if order.quantity == 0:
                        break

                    matching_orders = self.buy_order_book[price]
                    for buy_order in matching_orders:
                        if order.quantity == 0:
                            break

                        if buy_order.quantity <= order.quantity:
                            # Full match
                            print(f"Trade executed (IOC): {buy_order.quantity} at price {buy_order.price} to order_id={order.order_id}")
                            order.quantity -= buy_order.quantity
                            # Remove the first order in the list
                            self.update_Cumulative_quantity( matching_orders.pop(0),False)
                        else:
                            # Partial match
                            print(f"Trade executed (IOC): {order.quantity} at price {buy_order.price} to order_id={order.order_id}")
                            buy_order.quantity -= order.quantity
                          
                            order.quantity = 0
                            print("buyer cumu",self.buy_Cumulative_quantity)
                            self.update_Cumulative_quantity( buy_order,add=False,partial= True, partnum=  order.quantity)

                            return  # Cancel remaining IOC order

            elif order.condition == Condition.ROD:
                # Regular Order
                for price in matching_prices:
                    if order.quantity == 0:
                        break

                    matching_orders = self.buy_order_book[price]
                    for buy_order in matching_orders:
                        if order.quantity == 0:
                            break

                        if buy_order.quantity <= order.quantity:
                            # Full match
                            print(f"Trade executed (ROD): {buy_order.quantity} at price {buy_order.price} to order_id={order.order_id}")
                            order.quantity -= buy_order.quantity
                            self.update_Cumulative_quantity( matching_orders.pop(0),False) # Remove the first order in the list
                        else:
                            # Partial match
                            print(f"Trade executed (ROD): {order.quantity} at price {buy_order.price} to order_id={order.order_id}")
                            buy_order.quantity -= order.quantity
                            self.update_Cumulative_quantity( buy_order,add=False,partial= True, partnum=  order.quantity)
                            order.quantity = 0

                if order.quantity > 0:
                    # Add remaining quantity to the sell order book
                     
                    if order.price not in self.sell_order_book:
                        self.sell_order_book[order.price] = []
                    self.sell_order_book[order.price].append(order)
                    self.update_Cumulative_quantity(order)

                    
     
    def display_order_book(self):
        print("\nBuy Order Book:")
        print (self.buy_order_book)
        print (self.buy_Cumulative_quantity)
        for price, orders in self.buy_order_book.items():
            cumulative_quantity = sum(order.quantity for order in orders)
            print(f"Price: {price}, Cumulative Quantity: {cumulative_quantity}")

        print("\nSell Order Book:")
        print (self.sell_order_book)
        print (self.sell_Cumulative_quantity)

        for price, orders in self.sell_order_book.items():
            cumulative_quantity = sum(order.quantity for order in orders)
            print(f"Price: {price}, Cumulative Quantity: {cumulative_quantity}")


def main():
    order_book = OrderBook()

    # Example orders with conditions
    orders = [
        # Order('buy', 100, 5, Condition.FOK),    # Buy 5 at price 100 (FOK)
        # Order('buy', 113.4 , 6, Condition.ROD),    # Buy 4 at price 112 (FOK)
        # # Order('buy', 113, 4, Condition.ROD),    # Buy 4 at price 112 (FOK)
        # # Order('sell', 112, 8, Condition.ROD),   # Sell 8 at price 105 (ROD)
        # # Order('sell', 104, 8, Condition.ROD),   # Sell 8 at price 104 (ROD)
         
         
        Order('buy', 105, 10, Condition.ROD) ,
        Order('buy', 110, 5, Condition.ROD) ,

        
        Order('sell', 104, 14, Condition.ROD)

    ]

    for order in orders:
        order_book.process_order(order)

    print("\nFinal Trade Details:")
    # Add any remaining unmatched orders to the trade details (if needed)

    order_book.display_order_book()


if __name__ == "__main__":
    main()
