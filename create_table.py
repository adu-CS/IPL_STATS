import sqlite3

conn = sqlite3.connect('database.sqlite')
print("Connected to database successfully")

# Check if Players table exists
cursor = conn.cursor()
cursor.execute('''
    SELECT name FROM sqlite_master WHERE type='table' AND name='Players';
''')
table_exists = cursor.fetchone()

if not table_exists:
    conn.execute('''
        CREATE TABLE Players (
            name TEXT,
            runs INTEGER,
            avg REAL,
            sr REAL,
        )
    ''')
    print("Created table 'Players' successfully!")
else:
    print("Table 'Players' already exists.")
# Similar logic for Teams table
cursor.execute('''
    SELECT name FROM sqlite_master WHERE type='table' AND name='Teams';
''')
table_exists = cursor.fetchone()

if not table_exists:
    conn.execute('''
        CREATE TABLE Teams (
            id INTEGER PRIMARY KEY,
            name TEXT,
            team TEXT
        )
    ''')
    print("Created table 'Teams' successfully!")
else:
    print("Table 'Teams' already exists.")

cursor.execute("ALTER TABLE Players ADD COLUMN ply_id")
conn.close()
