import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('database.sqlite')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# SQL statement to delete the Teams table if it exists
sql_delete_table = """
                    DROP TABLE IF EXISTS Teams;
                   """

try:
    # Execute the SQL command to delete the Teams table
    cursor.execute(sql_delete_table)
    print("Teams table deleted successfully")
except sqlite3.Error as e:
    # Print an error message if there's any issue with the SQL execution
    print("Error deleting Teams table:", e)

# Commit the transaction and close the connection
conn.commit()
conn.close()
