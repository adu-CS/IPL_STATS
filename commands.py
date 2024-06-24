import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('database.sqlite')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Execute the DROP TABLE statement
cursor.execute("DROP TABLE IF EXISTS playsfor")

# Commit the changes
conn.commit()

# Close the connection
conn.close()
