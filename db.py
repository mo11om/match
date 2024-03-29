import sqlite3 
from order import Deal,Order
def get_orders_from_db():
    conn = sqlite3.connect('orders.db')  # Connect to the database
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders")  # Execute a query
    orders = cursor.fetchall()  # Fetch all rows of the query result

    conn.close()  # Close the connection

    order_book =order. OrderBook()
    for order in orders:
        order_type, price, quantity, condition = order
        order_book.pro_rata_order(Order(order_type, price, quantity, Condition[condition]))

    return order_book
 
def get_user_id(username_to_search, db_path='order.db'):
    """
    Retrieves the user ID for a given username from an SQLite database.

    Args:
        username_to_search (str): The username to search for.
        db_path (str): Path to the SQLite database file (default: 'mydatabase.db').

    Returns:
        int or None: The user ID if found, or None if no user with the given username exists.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute the SQL query
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username_to_search,))
        user_id = cursor.fetchone()

        # Close the database connection
        conn.close()

        return user_id[0] if user_id else None
    except sqlite3.Error as e:
        print(f"Error retrieving user ID: {e}")
        return None

def insert_deal(deal: Deal, db_path='order.db') -> bool:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO deals (user_id, order_id, order_type, price, quantity)
            VALUES (?, ?, ?, ?, ?)
        """, (deal.user, deal.order_id, deal.order_type, deal.price, deal.quantity))

        conn.commit()
        conn.close()

        return True
    except sqlite3.Error as e:
        print(f"Error inserting deal: {e}")
        return False
 
def get_deals_by_user(user_id, db_path='order.db'):
    """
    delete and get
    
    """
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute the SQL query to retrieve deals for the given user_id
        cursor.execute("""
            SELECT order_id, order_type, price, quantity, created_at
            FROM deals
            WHERE user_id = ?
        """, (user_id,))
        deals = cursor.fetchall()
        # cursor.execute("DELETE FROM deals WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return deals
    except sqlite3.Error as e:
        print(f"Error retrieving deals: {e}")
        return []
       
if __name__ == "__main__":
    # Example usage
    # target_username = 'JohnDoe'
    # user_id_result = get_user_id(target_username)
    # if user_id_result:
    #     print(f"User ID for {target_username}: {user_id_result}")
    # else:
    #     print(f"No user found with the username: {target_username}")
    # new_deal = Deal(user=123, order_id=12, order_type='buy', price=100.0, quantity=10)
    # if insert_deal(new_deal):
    #     print("Deal successfully inserted.")
    # else:
    #     print("Failed to insert deal.")
    user_id_to_search = 3
    user_deals = get_deals_by_user(user_id_to_search)
    if user_deals:
        print(f"Deals for user {user_id_to_search}:")
        for deal in user_deals:
            print(f"Order ID: {deal[0]}, Type: {deal[1]}, Price: {deal[2]}, Quantity: {deal[3]}, Created At: {deal[4]}")
    else:
        print(f"No deals found for user {user_id_to_search}.")