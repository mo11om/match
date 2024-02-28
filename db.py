import sqlite3

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