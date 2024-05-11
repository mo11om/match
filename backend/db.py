import sqlite3 ,datetime
from order import Deal
current_time = datetime.datetime.now()
cur_time=current_time
def table_init():
    """
    clean deal table

    """
    conn = sqlite3.connect('order.db')  # Connect to the database
    cursor = conn.cursor()

    cursor.execute("DELETE FROM deals")  # Execute a query
    conn.commit()
    conn.close()  # Close the connection
    return  
def get_all_users(db_path='order.db'):
  """
  Retrieves all users as a dictionary from an SQLite database.

  Args:
      db_path (str): Path to the SQLite database file (default: 'order.db').

  Returns:
      dict: A dictionary where keys are usernames and values are user IDs.
  """
  try:
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute the SQL query to fetch all users
    cursor.execute("SELECT username, user_id FROM users")
    users = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Create an empty dictionary to store users
    user_dict = {}

    # Build the dictionary with username as key and user ID as value
    for user in users:
      username, user_id = user
      user_dict[username] = user_id

    return user_dict

  except sqlite3.Error as e:
    print(f"Error retrieving users: {e}")
    return {}

user_dict=get_all_users()
deal_dict={}
 
def get_user_id(username_to_search, db_path='order.db'):
    """
    Retrieves the user ID for a given username from an SQLite database.

    Args:
        username_to_search (str): The username to search for.
        db_path (str): Path to the SQLite database file (default: 'mydatabase.db').

    Returns:
        int or None: The user ID if found, or None if no user with the given username exists.
    """
    if username_to_search in user_dict:
        return user_dict[username_to_search]
    else:
        return None
    # try:
    #     # Connect to the SQLite database
    #     conn = sqlite3.connect(db_path)
    #     cursor = conn.cursor()

    #     # Execute the SQL query
    #     cursor.execute("SELECT user_id FROM users WHERE username = ?", (username_to_search,))
    #     user_id = cursor.fetchone()

    #     # Close the database connection
    #     conn.close()

    #     return user_id[0] if user_id else None
    # except sqlite3.Error as e:
    #     print(f"Error retrieving user ID: {e}")
    #     return None

def insert_deal(deal: Deal, db_path='order.db') -> bool:
    if deal.user== get_user_id("market"):
       return True
    if deal.user not in deal_dict:
        deal_dict[deal.user] = []

    deal_dict[deal.user].append(deal)
    return True
    # try:
    #     conn = sqlite3.connect(db_path)
    #     cursor = conn.cursor()

    #     cursor.execute("""
    #         INSERT INTO deals (user_id, order_id, order_type, price, quantity,created_at)
    #         VALUES (?, ?, ?, ?, ?, ?)
    #     """, (deal.user, deal.order_id, deal.order_type, deal.price, deal.quantity,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    #     conn.commit()
    #     conn.close()

    #     return True
    # except sqlite3.Error as e:
        # print(f"Error inserting deal: {e}")
        # return False



def get_deals_by_user(user_id, db_path='order.db'):
    """
     get deals
    
    """
    # print(cur_time)
    return deal_dict.get(user_id, [])
    # try:
    #     conn = sqlite3.connect(db_path)
    #     cursor = conn.cursor()

    #     # Execute the SQL query to retrieve deals for the given user_id
    #     cursor.execute("""
    #         SELECT deal_id, order_type, price, quantity, created_at
    #         FROM deals
    #         WHERE user_id = ? AND created_at >= ?
    #         ORDER BY created_at DESC
                       
    #     """, (user_id,cur_time))
    #     deals = cursor.fetchall()
    #     conn.commit()
    #     conn.close()
    #     return deals
    # except sqlite3.Error as e:
    #     print(f"Error retrieving deals: {e}")
    #     return []
       
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