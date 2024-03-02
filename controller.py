from order import Order,Condition,OrderBook
import json
 

all_order=OrderBook()


 
    

    

def newOrder(order:Order):
     
    all_order. inputOrder(order)
    all_order.dealing()
    return order. get_order_id()


 
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
            order_type = order_data.get("order_type")
            price = order_data.get("price")
            quantity = order_data.get("quantity")
            condition = order_data.get("condition")
            market = order_data.get("market", False)  # Default to False if not specified

            try:
                condition_enum = Condition[condition]
            except KeyError:
                print("Invalid condition in the JSON file. Please use FOK, IOC, or ROD.")
                return None

            return newOrder(Order(user=user, order_type=order_type, price=price, quantity=quantity, condition=condition_enum, market=market))
    # except FileNotFoundError:
    #     print(f"File not found: {json_file_path}")
    #     return None
    except json.JSONDecodeError:
        print(f"Invalid JSON format in file")
        return None
    
def show_deal():
    while(not all_order.finish_deal.empty()):
        print(all_order.finish_deal.get())
def test():
    
   pass
     

        # Example usage: Read order details from "order.json" file
 
    
    
if __name__ == "__main__":
    
    test()
    