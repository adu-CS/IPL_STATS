import sqlite3

conn=sqlite3.connect('database.sqlite')
print("Connected to db")

cursor = conn.cursor()
cursor.execute('''
    SELECT name FROM sqlite_master WHERE type='table' AND name='playsfor';
''')

table_exists = cursor.fetchone()

if not table_exists:
    conn.execute('''
        CREATE TABLE playsfor(
            team_id INTEGER,
            team_name TEXT,
            ply_id INTEGER,
            ply_name TEXT,
            PRIMARY KEY (team_id, ply_id)
        )
    ''')
    print("Created table 'playsfor' successfully!")
else:
    print("Table 'playsfor' already exists.")


conn.close()
