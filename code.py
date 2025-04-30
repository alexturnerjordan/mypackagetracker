import datetime  # Used for handling estimated delivery times and order timestamps
import sqlite3  # Used to store order and tracking information locally
from sqlite3 import Error  # To catch SQL-related errors
from tabulate import tabulate  # Formats data in tables for better readability

database_file = "mypackagetracker.db"  # Renamed database to match project

def create_connection(db_file):
    """Establishes a connection to the SQLite database file provided."""
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print("Connection error:", e)
        return None

conn = create_connection(database_file)

if conn:
    print("✅ Connected to database.")
else:
    print("❌ Failed to connect to database.")

# Function to enter a new package order into the system
def input_order():
    order_details = []
    tracking_events = []

    package_id = input("Enter Package ID (e.g., ABC1234): ")
    while True:
        if package_id[:3].isalpha() and package_id[3:].isnumeric():
            break
        else:
            print("❌ Invalid Package ID format. Try again.")
            package_id = input("Enter Package ID (3 letters + 4 numbers): ")
    tracking_events.append(package_id)

    item_count = input("Enter number of items in the package: ")
    order_timestamp = datetime.datetime.now()

    # Calculate estimated delivery times
    if int(item_count) >= 3000:
        foreign_port = "Yan Tin"
        travel_stages = [0, 6, 14, 3, 2, 6]
    elif int(item_count) >= 500:
        foreign_port = "Sihanoukville"
        travel_stages = [0, 5, 12, 3, 2, 6]
    else:
        print("Minimum order = 200 items.")
        item_count = input("Enter a valid item count: ")

current_time = order_timestamp
    for days in travel_stages:
        next_stage_time = current_time + datetime.timedelta(days=days)
        tracking_events.append(next_stage_time.strftime("%x"))
        current_time = next_stage_time

    order_details = list((package_id, order_timestamp.strftime("%x"), item_count, foreign_port, tracking_events[2], tracking_events[-1]))

try:
        conn.execute("INSERT INTO orders (crid, dateplaced, units, portoforigin, edd, eda) VALUES (?, ?, ?, ?, ?, ?)", order_details)
        conn.execute("INSERT INTO trackorder (crid, orderplaced, departorigin, arrivedomestic, offload, readyintermodal, arrivedc) VALUES (?, ?, ?, ?, ?, ?, ?)", tracking_events)
        conn.commit()
     print("Order saved to the database.")
    except Error as e:
        print("Error saving order:", e)
       
       
        def retrieve_order(package_id=None):
    try:
        if package_id:
            cursor = conn.execute("SELECT * FROM orders WHERE crid = ?", (package_id,))
        else:
            cursor = conn.execute("SELECT * FROM orders")
        
        headers = [col[0].upper() for col in cursor.description]
        orders = [headers]

        for row in cursor:
            orders.append(list(row))

        return orders

    except Error as e:
        print("❌ Error retrieving order:", e)
        return []
# Function to retrieve tracking events for a given package

def retrieve_tracking(package_id=None):
    try:
        if package_id:
            cursor = conn.execute("SELECT * FROM trackorder WHERE crid = ?", (package_id,))
        else:
            cursor = conn.execute("SELECT * FROM trackorder")

        headers = [col[0].upper() for col in cursor.description]
        tracking_info = [headers]

        for row in cursor:
            tracking_info.append(list(row))

        return tracking_info

    except Error as e:
        print("❌ Error retrieving tracking info:", e)
        return []
