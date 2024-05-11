from sortedcontainers import SortedDict
from enum import Enum
from time import time
from queue import Queue
inf= float("inf")
ninf=float("-inf")
class Condition(Enum):
    FOK = 1  # Fill or Kill
    IOC = 2  # Immediate or Cancel
    ROD = 3  # Regular Order


class Order:
    order_counter = 0  # A class variable to assign unique order IDs

    def __init__(self, user:str,order_type:str, price:float, quantity:int, condition:Condition,market=False)->int:
        """
        Initializes an Order object.

        Args:
            user (str): User associated with the order.
            order_type (str): 'buy' or 'sell'.
            price (float): Price of the order.
            quantity (int): Quantity of the order.
            condition (Condition): Condition of the order (FOK, IOC, ROD).
            market (bool, optional): Whether the order is a market order. Defaults to False.
        """
        self.user=user
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
        return f"Order(user={self.user} order_id={self.order_id}, order_type='{self.order_type}', price={self.price}, quantity={self.quantity}, timestamp={self.timestamp}, condition={self.condition})"


class Deal:
    order_counter = 0  # A class variable to assign unique order IDs

    def __init__(self,user, order_id:int,order_type, price, quantity:int)->None:
        
        self.user=user
        self.order_id = order_id  # Unique order ID
        self.order_type = order_type  # 'buy' or 'sell' 
        self.price = price
        self.quantity = quantity
        self.timestamp = int(time())  # Current timestamp
  
    def get_order_id(self):
        return self.order_id
    def __dict__(self):
        return {
            "price": self.price,
            "quantity": self.quantity,
            "user": self.user,
            "order_id": self.order_id,
            "order_type": self.order_type,
            "timestamp": self.timestamp,
        }
    def __repr__(self):
        return f"Order(user={self.user} ,order_type={self.order_type},order_id={self.order_id} , price={self.price}, quantity={self.quantity}, timestamp={self.timestamp} )"


class OrderBook:
    def __init__(self):
        self.buy_order_book = SortedDict()
        self.buy_Cumulative_quantity=SortedDict()
        self.sell_order_book = SortedDict()
        self.sell_Cumulative_quantity=SortedDict()
        self.trade_Cumulative_quantity=SortedDict()
        self.trade_price=inf
        self.finish_deal=Queue()
        self.inOrder=Queue()
        
    def check_fill_or_kill(self ,order:Order )->bool:
        # self.update_Cumulative_quantity()
        matching_prices = self.get_matching_prices(order)

        # print ("matching_prices",matching_prices)
        test_quantity=order.quantity
        
        
        for price in matching_prices:
            # print("test_quantity",test_quantity)
            if test_quantity <= 0:
                return True
            orders = self.sell_order_book[price] if order.order_type == 'buy' else self.buy_order_book[price]
            # self.fifo_match(matching_orders, order) 
            cumulative_quantity = sum(order.quantity for order in orders)   
            test_quantity-=cumulative_quantity    
            if test_quantity <= 0:
                    return True
        
        return False
        
         


       
    def update_Cumulative_quantity(self  ):  
        """Calculates and updates the cumulative quantity for both buy and sell orders.

        Updates `self.buy_Cumulative_quantity` and `self.sell_Cumulative_quantity` dictionaries
        with the cumulative quantity for each price level in the order books. Removes entries from
        these dictionaries when the cumulative quantity becomes 0.
        """
        for order_book, cumulative_quantity_dict in (
        (self.buy_order_book, self.buy_Cumulative_quantity),
        (self.sell_order_book, self.sell_Cumulative_quantity),
        ):
            for price, orders in order_book.items():
                total_quantity = sum(order.quantity for order in orders)
                if total_quantity > 0:
                    cumulative_quantity_dict[price] = total_quantity
                else:
                    cumulative_quantity_dict.pop(price, None)  # Remove entry if quantity is 0

        # for price, orders in self.buy_order_book.items():
        #     cumulative_quantity = sum(order.quantity for order in orders)
        #     if cumulative_quantity:
        #             self.buy_Cumulative_quantity[price]=cumulative_quantity
        #     else :
        #         self.buy_Cumulative_quantity[price]=0
        # print("buy_Cumulative_quantity",self.buy_Cumulative_quantity)

        
        # for price, orders in self.sell_order_book.items():
        #     cumulative_quantity = sum(order.quantity for order in orders)
        #     if cumulative_quantity>0:
        #         self.sell_Cumulative_quantity[price]=cumulative_quantity
        #     elif cumulative_quantity==0 :
        #         self.sell_Cumulative_quantity[price]=0
            

        # print("sell_Cumulative_quantity",self.sell_Cumulative_quantity)


 


    def add_finish_deal(self,order1:Order,order2:Order,price,quantity):
        if quantity>0:
            self.finish_deal.put(Deal(order1.user,order1.order_id,order1.order_type,price,quantity))
            self.finish_deal.put(Deal(order2.user,order2.order_id,order2.order_type,price,quantity))
            self.trade_price=price
            if price not in self.trade_Cumulative_quantity:
                    self.trade_Cumulative_quantity[ price] =    quantity
            else:
                    self.trade_Cumulative_quantity[ price]+= quantity

                
    def fifo_match(self,matched_orders:list,order:Order):
        if order.quantity == 0:
            return  # No need to process further
        
        index=0  
        while index < len(matched_orders) and order.quantity > 0:
            matched_order :Order= matched_orders[index]

            matched_quantity = min(matched_order.quantity, order.quantity)
            self.add_finish_deal(matched_order, order, price=matched_order.price, quantity=matched_quantity)

            if matched_quantity == matched_order.quantity:
                print(f"Trade executed FULL (ROD): {matched_quantity} at price {matched_order.price} to order_id={order.order_id}")
                # self.update_Cumulative_quantity(matched_order, False)  # Remove the first order
                index += 1
            else:
                print(f"Trade executed PART (ROD): {matched_quantity} at price {matched_order.price} to order_id={order.order_id}")
                # self.update_Cumulative_quantity(matched_order, add=False, partial=True, partnum=order.quantity)
                matched_order.quantity-=order.quantity
            order.quantity -= matched_quantity
            

        if index == len(matched_orders):
            del matched_orders[:]  # Clear the entire list
        else:
            del matched_orders[:index]  # Remove elements up to (but not including) index

    def pro_rata_match(self,matched_orders:list,order:Order):
        total_quantity = sum(order.quantity for order in matched_orders)
        if order.quantity>total_quantity:
            self.fifo_match(matched_orders=matched_orders,order=order)
            return
        elif order.quantity>0: 
            matched_order:Order
            print("total_quantity",total_quantity)
            print("order quantity", order.quantity)
            estimate_minus_ratio=order.quantity/total_quantity
            print("ratio",estimate_minus_ratio)
            for matched_order in matched_orders[:]:
                
                matched_quantity=min(matched_order.quantity,int(estimate_minus_ratio*matched_order.quantity) )
                print(matched_quantity)
                self.add_finish_deal(matched_order, order, price=matched_order.price, quantity=matched_quantity)

                matched_order.quantity-=matched_quantity
                order.quantity-= matched_quantity

                if matched_order.quantity == 0:
                    matched_orders.remove(matched_order)

             
                


            if order.quantity<=0:
                return
            
        self.fifo_match(matched_orders=matched_orders,order=order)

        return    
     
    def process_order(self, order):
        # print(order)
        if order.order_type == 'buy':
             
            if order.condition == Condition.FOK:
                if not self.check_fill_or_kill(order):
                    print(f"FOK order canceled: order_id={order.order_id}")
                    return
            
            self.handle_order(order)
            
        elif order.order_type == 'sell':
             
            if order.condition == Condition.FOK:
                if not self.check_fill_or_kill(order):
                    print(f"FOK order canceled: order_id={order.order_id}")
                    return
            self.handle_order(order)
            

    def handle_order(self, order:Order):
        matching_prices = self.get_matching_prices(order)
        # print ("matching_prices",matching_prices)
        for price in matching_prices:
             
            if order.quantity == 0:
                break
            matching_orders = self.sell_order_book[price] if order.order_type == 'buy' else self.buy_order_book[price]
            self.pro_rata_match(matching_orders, order)
        if order.quantity>0:
            self.add_order(order=order)
    def add_order(self,order:Order):
        if order.order_type=="buy":
            self.buy_order_book.setdefault(order.price, []).append(order)
        elif order.order_type=="sell":
             self.sell_order_book.setdefault(order.price, []).append(order)
             
    def get_matching_prices(self, order):
        if order.order_type == 'buy':
            return self.sell_order_book.irange(maximum=order.price)
        else:
            return self.buy_order_book.irange(minimum=order.price)               
    
   
    
        
     
    def inputOrder(self,order:Order):
        self.inOrder.put(order)
    def dealing(self):
        while(not self.inOrder.empty()):
            self.process_order(self.inOrder.get())
        pass              
     
    def display_order_book(self):
        print("\nBuy Order Book:")
        print (self.buy_order_book)
        # print (self.buy_Cumulative_quantity)
        for price, orders in self.buy_order_book.items():
            cumulative_quantity = sum(order.quantity for order in orders)
            print(f"Price: {price}, Cumulative Quantity: {cumulative_quantity}")

        print("\nSell Order Book:")
        print (self.sell_order_book)
        # print (self.sell_Cumulative_quantity)

        for price, orders in self.sell_order_book.items():
            cumulative_quantity = sum(order.quantity for order in orders)
            
            print(f"Price: {price}, Cumulative Quantity: {cumulative_quantity}")




def main( ):
    
    order_book = OrderBook()
    
     
    orders = [
        # Order('buy', 100, 5, Condition.FOK),    # Buy 5 at price 100 (FOK)
        # Order('buy', 113.4 , 6, Condition.ROD),    # Buy 4 at price 112 (FOK)
        # # Order('buy', 113, 4, Condition.ROD),    # Buy 4 at price 112 (FOK)
        # # Order('sell', 112, 8, Condition.ROD),   # Sell 8 at price 105 (ROD)
        # # Order('sell', 104, 8, Condition.ROD),   # Sell 8 at price 104 (ROD)
         
        Order(1,'buy', 110, 20, Condition.ROD) ,
        Order(2,'buy', 110, 40, Condition.ROD) ,
       
        Order(3,'sell', 109, 40, Condition.FOK) ,
       
    #    Order(1,'sell', 110, 30, Condition.ROD) ,
        
       
        
    #     Order(2,'buy', 118,70, Condition.FOK),


    ]
    # Example orders with conditions 
    for order in orders:
        order_book. inputOrder(order)

    order_book.dealing()
    
    print("\nFinal Trade Details:")
    # Add any remaining unmatched orders to the trade details (if needed)
    print("remain in  order_book ")
    order_book.display_order_book()
    # print(orders)
 
    
    # #order_book.display_order_book()
    print("\n trade \n")
    while(not order_book.finish_deal.empty()):
        print(order_book.finish_deal.get())
    print(order_book.trade_Cumulative_quantity)
 
if __name__ == "__main__":
    
    
    
    
    
    main( )

    
    
