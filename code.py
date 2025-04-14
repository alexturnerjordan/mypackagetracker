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
