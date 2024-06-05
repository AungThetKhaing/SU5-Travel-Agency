import mysql.connector

# Establish a database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",  # If your MySQL database has no password
)

print(mydb)
print("Connection is ok")

# Create a cursor object
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE SUM5TA")
#mycursor.execute("DROP DATABASE SUM5TA")
mydb.commit()
print("Database successfully created.")

# Close the cursor and connection
mycursor.close()
mydb.close()
