import sqlite3

conn = sqlite3.connect('database.sqlite')
print("Connected to database successfully")

# Check if Matches table exists
cursor = conn.cursor()
cursor.execute('''
    SELECT name FROM sqlite_master WHERE type='table' AND name='Matches';
''')
table_exists = cursor.fetchone()

if not table_exists:
    # Create the Matches table
    conn.execute('''
        CREATE TABLE Matches (
            match_id INTEGER PRIMARY KEY,
            tournament_id INTEGER NOT NULL,
            team1_id INTEGER NOT NULL,
            team2_id INTEGER NOT NULL,
            match_date TEXT NOT NULL,
            venue TEXT NOT NULL,
            result TEXT,
            winning_team_id INTEGER,
            losing_team_id INTEGER,
            FOREIGN KEY (tournament_id) REFERENCES Tournaments(tournament_id),
            FOREIGN KEY (team1_id) REFERENCES Teams(team_id),
            FOREIGN KEY (team2_id) REFERENCES Teams(team_id),
            FOREIGN KEY (winning_team_id) REFERENCES Teams(team_id),
            FOREIGN KEY (losing_team_id) REFERENCES Teams(team_id)
        )
    ''')
    print("Created table 'Matches' successfully!")
else:
    print("Table 'Matches' already exists.")

# Close the database connection
conn.close()
