from order import Order,Condition,OrderBook
import db


import json
 

all_order=OrderBook()
#clean deals
#db.table_init()
    

    

def newOrder(order:Order):
    """
    send new order
    name is id from get_user_id
    """
     
    all_order. inputOrder(order)
    all_order.dealing()
    while(not all_order.finish_deal.empty()):
        deal=all_order.finish_deal.get()
        print(deal)
        db.insert_deal(deal)
    return order. get_order_id()

def get_user_id(user:str):
    "get user_id"
    user_id=db.get_user_id(user)
    return user_id
 
def input_order_from_json(order_data):
    """
    Reads order details from a JSON file and returns an Order object.

    Args:
        json_file_path (str): Path to the JSON file containing order details.

    Returns:
        Order: An Order object with attributes from the JSON file.
    """
    try:
         
             
            user = order_data.get("user")
            
            user_id= get_user_id(user)
            
            if user_id is None:
                raise ValueError("User does not exist")
            
            order_type = order_data.get("order_type")
           
            price = order_data.get("price")
            quantity = order_data.get("quantity")
            condition = order_data.get("condition")
            # if order_type is not  Condition:
            #     raise ValueError("condition does not have %s",order_type)
            market = order_data.get("market", False)  # Default to False if not specified

            try:
                condition_enum = Condition[condition]
            except KeyError:
                print("Invalid condition in the JSON file. Please use FOK, IOC, or ROD.")
                return None

            return newOrder(Order(user=user_id, order_type=order_type, price=price, quantity=quantity, condition=condition_enum, market=market))
    # except FileNotFoundError:
    #     print(f"File not found: {json_file_path}")
    #     return None
    except json.JSONDecodeError:
        print(f"Invalid JSON format in file")
        return None
def get_deal(user):
    """
    get result from user name
    """
    user_id=db.get_user_id(user)
    if user_id is None:
        raise ValueError("User does not exist")
            
    deals=db.get_deals_by_user(user_id)
    # print(deals)
    return deals
       
def show_deal():
    # while(not all_order.finish_deal.empty()):
    #     print(all_order.finish_deal.get())
        # Convert the queue to a list
    queue_list = list(all_order.finish_deal)
    print("q list",queue_list)
    # Print the elements from the list
    for item in queue_list:
        print(item)
def get_trade_price():
    print(all_order.trade_price)
    if all_order.trade_price== float("inf"):
        return None
    return all_order.trade_price
def get_quantity():
    print("result")
    # print(all_order.buy_order_book)
    # print(all_order.sell_order_book)
    print(all_order.buy_Cumulative_quantity)
    print(all_order.sell_Cumulative_quantity)
    
    return  {"buy":all_order.buy_Cumulative_quantity,"sell":all_order.sell_Cumulative_quantity}
def test():
    
   pass
     

        # Example usage: Read order details from "order.json" file
 
    
    
if __name__ == "__main__":
    
    test()
    