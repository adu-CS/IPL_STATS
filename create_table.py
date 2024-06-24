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
    # Create the Teams table
    conn.execute('''
        CREATE TABLE Teams (
            team_id INTEGER PRIMARY KEY,
            team_name VARCHAR(255),
            manager_id INTEGER,
            manager_name VARCHAR(255),
            contact_email VARCHAR(255),
            tournament_id INTEGER,
            FOREIGN KEY (tournament_id) REFERENCES Tournaments(tournament_id)
        )
    ''')
    print("Created table 'Teams' successfully!")
else:
    print("Table 'Teams' already exists.")

cursor.execute("ALTER TABLE Players ADD COLUMN ply_id")
conn.close()
