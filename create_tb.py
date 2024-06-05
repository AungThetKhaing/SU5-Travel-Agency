import mysql.connector

# Establish a database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",  # If your MySQL database has no password
    database="SUM5TA"
)

print(mydb)
print("Connection is ok")

# Create a cursor object
mycursor = mydb.cursor()

create_customer_table= """
CREATE TABLE IF NOT EXISTS customer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    passport TEXT NOT NULL,
    address TEXT
)
"""

create_trip_table = """
CREATE TABLE IF NOT EXISTS trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination TEXT NOT NULL,
    option TEXT NOT NULL,
    hotel TEXT NOT NULL,
    duration INTEGER NOT NULL,
    price REAL NOT NULL
)
"""
create_booking_table = """
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    trip_id INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (id),
    FOREIGN KEY (trip_id) REFERENCES trips (id)
)
"""
try:
    mycursor.execute(create_customer_table)
    print("Customer Table created successfully")
    mycursor.execute(create_trip_table)
    print("Trip Table created successfully")
    mycursor.execute(create_booking_table)
    print("Booking Table created successfully")
    mydb.commit()  # Commit the transactions
    print("Tables created successfully")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    
# Close the cursor and connection
mycursor.close()
mydb.close()
