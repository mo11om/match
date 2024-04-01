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
                    print("Update_part",self.buy_Cumulative_quantity)
                    self.buy_Cumulative_quantity[order.price]-=partnum
                    print("Update_part",self.buy_Cumulative_quantity)

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
    def add_finish_deal(self,order1:Order,order2:Order,price,quantity):
        if quantity>0:
            self.finish_deal.put(Deal(order1.user,order1.order_id,order1.order_type,price,quantity))
            self.finish_deal.put(Deal(order2.user,order2.order_id,order2.order_type,price,quantity))
            self.trade_price=price
            if price not in self.trade_Cumulative_quantity:
                    self.trade_Cumulative_quantity[ price] =    quantity
            else:
                    self.trade_Cumulative_quantity[ price]+= quantity

                
    def time_match(self,order_list:list,order:Order):
       
        index=0 

        for buy_order in order_list:
              
            if order.quantity == 0:
                break

            if buy_order.quantity <= order.quantity:
                # Full match
                self.add_finish_deal (buy_order,order,price=buy_order.price,quantity=buy_order.quantity)
               
                
                print(f"Trade executed FULL (ROD): {buy_order.quantity} at price {buy_order.price} to order_id={order.order_id}")
                order.quantity -= buy_order.quantity
                

                self.update_Cumulative_quantity( buy_order,False) # Remove the first order in the list
                index = index+1
 

            else:
                # Partial match
   
                self.add_finish_deal(buy_order,order,price=buy_order.price,quantity=order.quantity)
                print(f"Trade executed PART (ROD): {order.quantity} at price {buy_order.price} to order_id={order.order_id}")
                buy_order.quantity -= order.quantity
                self.update_Cumulative_quantity( buy_order,add=False,partial= True, partnum=  order.quantity)
                order.quantity = 0
            
            
        if index == len(order_list):
            order_list.clear()
            
        else:
            for _ in range(index):
                    order_list.pop(0)
        
    def process_order(self, order:Order):
         
        if order.order_type == 'buy':
            # Look for matching sell orders
            matching_prices = self.sell_order_book.irange(maximum=order.price,   )  # Get prices less than or equal to buy order price
             
            if order.condition == Condition.FOK:
                # FOK (Fill or Kill) order should execute fully or not at all
                
                if (self.check_fill_or_kill(order)):
                    for price in matching_prices:
                        
                        if order.quantity == 0:
                            break
                        
                        matching_orders = self.sell_order_book[price]
                        self.time_match(matching_orders,order)
                else:
                    print(f"FOK order canceled: order_id={order.order_id}")
                    return    

            elif order.condition == Condition.IOC:
                # IOC (Immediate or Cancel) order should execute as much as possible and cancel the rest

                for price in matching_prices:
                  
                    if order.quantity == 0:
                        break
                      
                    matching_orders = self.sell_order_book[price]
                    self.time_match(matching_orders,order)
            elif order.condition == Condition.ROD:
                # Regular Order
               
                for price in matching_prices:
                    
                    if order.quantity == 0:
                        break
                    matching_orders =self.sell_order_book[price]
                    
                    self.time_match(matching_orders,order=order)
    
                    # for sell_order in matching_orders:
                    #     if order.quantity == 0:
                    #         break

                    #     if sell_order.quantity <= order.quantity:
                    #         # Full match
                    #         print(f"Trade executed (ROD): {sell_order.quantity} at price {sell_order.price} to order_id={order.order_id}")
                    #         order.quantity -= sell_order.quantity
                    #         self.update_Cumulative_quantity( matching_orders.pop(0),False)  # Remove the first order in the list
                    #     else:
                    #         # Partial match
                    #         print(f"Trade executed (ROD): {order.quantity} at price {sell_order.price} to order_id={order.order_id}")
                    #         sell_order.quantity -= order.quantity
                    #         self.update_Cumulative_quantity( sell_order,add=False,partial= True, partnum= order.quantity)
                    #         order.quantity = 0

                if order.quantity > 0:
                    # Add remaining quantity to the buy order book
                    if order.price not in self.buy_order_book:
                        self.buy_order_book[order.price] = []
                    self.buy_order_book[order.price].append(order)
                    self.update_Cumulative_quantity(order)
                    

        elif order.order_type == 'sell':
            # Look for matching buy orders
            matching_prices = self.buy_order_book.irange(minimum=order.price)  # Get prices greater than or equal to sell order price

            if order.condition == Condition.FOK:
                # FOK (Fill or Kill) order should execute fully or not at all
                if (self.check_fill_or_kill(order)) :
                    #
                    for price in matching_prices:
                        if order.quantity == 0:
                            break

                        matching_orders = self.buy_order_book[price]
                        self.time_match(matching_orders,order)
                         
                else:
                    print(f"FOK order canceled: order_id={order.order_id}")
                    return     
            elif order.condition == Condition.IOC:
                # IOC (Immediate or Cancel) order should execute as much as possible and cancel the rest
    
                for price in matching_prices:
                    if order.quantity == 0:
                        break

                    matching_orders = self.buy_order_book[price]
                    self.time_match(matching_orders,order)
                    
            elif order.condition == Condition.ROD:
                # Regular Order
                for price in matching_prices:
                    if order.quantity == 0:
                        break

                    matching_orders = self.buy_order_book[price]
                    self.time_match(matching_orders,order)
                  
                if order.quantity > 0:
                    # Add remaining quantity to the sell order book
                     
                    if order.price not in self.sell_order_book:
                        self.sell_order_book[order.price] = []
                    self.sell_order_book[order.price].append(order)
                    self.update_Cumulative_quantity(order)
    
    def get_pro_rata_price(self,order:Order):
        if order.order_type=="buy":
            tmp=order.quantity
            last_price=None
           
            print(self.sell_Cumulative_quantity)
            for key,value in self.sell_Cumulative_quantity.items():
                if  key> order.price:
                    break 
                tmp=tmp-value
                last_price=key 
                if tmp <= 0:
                    break
            print("last",last_price)
            if tmp>0:
                last_price=inf
            return last_price
             
        if order.order_type=="sell":
            tmp=order.quantity
            last_price=None
           
            print(self.buy_Cumulative_quantity)
            for key,value in self.buy_Cumulative_quantity.items():
                print("cumulative",key)
                if  key< order.price:
                    continue 
                tmp=tmp-value
                  
                last_price=key 
                if tmp <= 0:
                    
                    break
            print("last",last_price)
            if self.buy_Cumulative_quantity:
                if last_price ==self.buy_Cumulative_quantity.peekitem(index=-1)[0] and tmp >0:
                    last_price=inf
            return last_price
    def pro_rata_match(self,matching_orders, total_sell_quantity,order:Order):
        total_buy_quantity = order.quantity
        for sell_order in matching_orders:
            allocation_ratio = min(sell_order.quantity / total_sell_quantity, 1.0)

            trade_quantity = int(total_buy_quantity * allocation_ratio)
            
            print ("allocation_ratio",allocation_ratio)
            print ("trade_quantity",trade_quantity)
            if trade_quantity > 0:
                # Partial match
                self.add_finish_deal(order,sell_order,price= order.price,quantity=trade_quantity)
                
                print(f"Trade executed (Pro-Rata): {trade_quantity} at price {sell_order.price} seller_id {sell_order.order_id} to buyer order_id={order.order_id}")
                sell_order.quantity -= trade_quantity
                order.quantity -= trade_quantity
                self.update_Cumulative_quantity( sell_order,add=False,partial= True, partnum= trade_quantity)
    def pro_rata_order(self, order:Order):
     
         
        if order.order_type == 'buy':
            # Look for matching sell orders
            matching_prices = self.sell_order_book.irange(maximum=order.price,  )  # Get prices less than or equal to buy order price
             
            if order.condition == Condition.FOK:
                # FOK (Fill or Kill) order should execute fully or not at all
                
                if (self.check_fill_or_kill(order)):
                    last_price= self.get_pro_rata_price(order)
                    for price in matching_prices:
                        
                        if order.quantity == 0:
                            break
                        
                        matching_orders = self.sell_order_book[price]
                        if price< last_price:
                            self.time_match(matching_orders,order)
                        
                        else:
                            # pro rata algo
                            total_sell_quantity = self.sell_Cumulative_quantity[last_price]
                            # total_buy_quantity= order.quantity
                            self.pro_rata_match(matching_orders,total_sell_quantity,order)
                        #remain
                            if order.quantity>0 and self.sell_Cumulative_quantity[last_price] >0:
                                self.time_match(matching_orders,order)
                         
                else:
                    print(f"FOK order canceled: order_id={order.order_id}")
                    return    

            # if order.condition == Condition.IOC:
            #     # IOC (Immediate or Cancel) order should execute as much as possible and cancel the rest

            #     for price in matching_prices:
                  
            #         if order.quantity == 0:
            #             break
                      
            #         matching_orders = self.sell_order_book[price]
            #         for sell_order in matching_orders:
            #             if order.quantity == 0:
            #                 break

            #             if sell_order.quantity <= order.quantity:
            #                 # Full match
            #                 print(f"Trade executed (IOC): {sell_order.quantity} at price {sell_order.price} seller_id {sell_order.order_id}  to buyer order_id={order.order_id}")
            #                 order.quantity -= sell_order.quantity
            #                 self.update_Cumulative_quantity( matching_orders.pop(0),False)  # Remove the first order in the list
            #             else:
            #                 # Partial match
            #                 print(f"Trade executed (IOC): {order.quantity} at price {sell_order.price} seller_id {sell_order.order_id}  to buyer  to order_id={order.order_id}")
            #                 sell_order.quantity -= order.quantity
                             
            #                 self.update_Cumulative_quantity( sell_order,add=False,partial= True, partnum= order.quantity)
            #                 order.quantity = 0
            #                 return  # Cancel remaining IOC order
            
            if order.condition == Condition.ROD or order.condition ==Condition.IOC:
                # Regular Order
                last_price=self.get_pro_rata_price(order)
                print ( last_price)
                
                for price in matching_prices:
                    print ("compare", price ,last_price)
                    if order.quantity == 0:
                        break

                    matching_orders = self.sell_order_book[price]
                    if price< last_price:
                        self.time_match(matching_orders,order)
                        # # for sell_order in matching_orders:
                        # #     if order.quantity == 0:
                        # #         break

                        # #     if sell_order.quantity <= order.quantity:
                        # #         # Full match
                        # #         print(f"Trade executed (ROD): {sell_order.quantity} at price {sell_order.price} to order_id={order.order_id}")
                        # #         order.quantity -= sell_order.quantity
                        # #         self.update_Cumulative_quantity( matching_orders.pop(0),False)  # Remove the first order in the list
                    
                    else:
                        # pro rata algo
                        total_sell_quantity = self.sell_Cumulative_quantity[last_price]
                        # total_buy_quantity= order.quantity
                        self.pro_rata_match(matching_orders,total_sell_quantity,order)
                       #remain
                        if order.quantity>0 and self.sell_Cumulative_quantity[last_price] >0:
                            self.time_match(matching_orders,order)


                if order.quantity > 0 and order.condition ==Condition.ROD:
                    
                    # Add remaining quantity to the buy order book
                    if order.price not in self.buy_order_book:
                        self.buy_order_book[order.price] = []
                    self.buy_order_book[order.price].append(order)
                    self.update_Cumulative_quantity(order)
                    

        elif order.order_type == 'sell':
            # Look for matching buy orders
            matching_prices = self.buy_order_book.irange(minimum=order.price, reverse=True)  # Get prices greater than or equal to sell order price
  
            matching_prices = list(matching_prices) 
            matching_prices.reverse()
        
        
            if order.condition == Condition.FOK:
                # FOK (Fill or Kill) order should execute fully or not at all
                if (self.check_fill_or_kill(order)) :
                    #
                    last_price=self.get_pro_rata_price(order)
                    for price in matching_prices:
                        if order.quantity == 0:
                            break

                        matching_orders = self.buy_order_book[price]
                        if price< last_price:
                            self.time_match(matching_orders,order)
                        else:
                            total_buy_quantity = self.buy_Cumulative_quantity[last_price]
                            self.pro_rata_match(matching_orders,total_buy_quantity,order)
                            
                            if order.quantity>0 and self.buy_Cumulative_quantity[last_price] >0:
                                self.time_match(matching_orders,order)
                else:
                    print(f"FOK order canceled: order_id={order.order_id}")
                    return     
            
            # if order.condition == Condition.IOC:
            #     # IOC (Immediate or Cancel) order should execute as much as possible and cancel the rest
            #     last_price=self.get_pro_rata_price(order)
            #     for price in matching_prices:
            #         if order.quantity == 0:
            #             break

            #         matching_orders = self.buy_order_book[price]
                

            #         if price< last_price:
            #             self.time_match(matching_orders,order)
            #         else:
            #             total_buy_quantity = self.buy_Cumulative_quantity[last_price]
            #             self.pro_rata_match(matching_orders,total_buy_quantity,order)
                        
            #             if order.quantity>0 and self.buy_Cumulative_quantity[last_price] >0:
            #                 self.time_match(matching_orders,order)

    

            if order.condition ==Condition.ROD or order.condition == Condition.IOC:
               
                # print(last_price)
                # Regular Order
                last_price=self.get_pro_rata_price(order)
                for price in matching_prices:
                   
                    if order.quantity == 0:
                        break
                

                    matching_orders = self.buy_order_book[price]
                    if price< last_price:
                        self.time_match(matching_orders,order)
                    else:
                        total_buy_quantity = self.buy_Cumulative_quantity[last_price]
                        self.pro_rata_match(matching_orders,total_buy_quantity,order)
                        
                        #remain time
                        if order.quantity>0 and self.buy_Cumulative_quantity[last_price] >0:
                            self.time_match(matching_orders,order)



                if order.condition==Condition.ROD and order.quantity > 0:
                    # Add remaining quantity to the sell order book
                    
                     
                    if order.price not in self.sell_order_book:
                        self.sell_order_book[order.price] = []
                    self.sell_order_book[order.price].append(order)
                    self.update_Cumulative_quantity(order)
    
    
        
     
    def inputOrder(self,order:Order):
        self.inOrder.put(order)
    def dealing(self):
        while(not self.inOrder.empty()):
            self.pro_rata_order(self.inOrder.get())
        pass              
     
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




def main( ):
    
    order_book = OrderBook()
    
     
    orders = [
        # Order('buy', 100, 5, Condition.FOK),    # Buy 5 at price 100 (FOK)
        # Order('buy', 113.4 , 6, Condition.ROD),    # Buy 4 at price 112 (FOK)
        # # Order('buy', 113, 4, Condition.ROD),    # Buy 4 at price 112 (FOK)
        # # Order('sell', 112, 8, Condition.ROD),   # Sell 8 at price 105 (ROD)
        # # Order('sell', 104, 8, Condition.ROD),   # Sell 8 at price 104 (ROD)
         
          Order(1,'buy', 110, 20, Condition.ROD) ,
          Order(2,'buy', 110, 20, Condition.ROD) ,
       
        Order(3,'sell', 109, 20, Condition.ROD) ,
       
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
    print("trade")
    while(not order_book.finish_deal.empty()):
        print(order_book.finish_deal.get())
    print(order_book.trade_Cumulative_quantity)
 
if __name__ == "__main__":
    
    
    
    
    
    main( )

    
    
