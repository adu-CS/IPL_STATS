import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('database.sqlite')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the ballbyball table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ballbyball (
        ball_id INTEGER PRIMARY KEY,
        match_id INTEGER,
        inning INTEGER,
        over_number INTEGER,
        ball_number INTEGER,
        batter_id INTEGER,
        bowler_id INTEGER,
        runs_scored INTEGER DEFAULT 0,
        extras INTEGER DEFAULT 0,
        wicket_type VARCHAR(50) DEFAULT 'NONE',
        fielder_id INTEGER DEFAULT NULL,
        FOREIGN KEY (match_id) REFERENCES matches(match_id),
        FOREIGN KEY (batter_id) REFERENCES players(player_id),
        FOREIGN KEY (bowler_id) REFERENCES players(player_id),
        FOREIGN KEY (fielder_id) REFERENCES players(player_id)
    )
''')

import sqlite3

def get_total_runs_scored():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(runs_scored) AS total_runs_scored FROM ballbyball")
    total_runs_scored = cursor.fetchone()[0]  # Fetch the result of the query
    conn.close()
    return total_runs_scored

def get_total_wickets_taken():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS total_wickets_taken FROM ballbyball WHERE wicket_type != 'NONE'")
    total_wickets_taken = cursor.fetchone()[0]  # Fetch the result of the query
    conn.close()
    return total_wickets_taken

# Example usage:
total_runs_scored = get_total_runs_scored()
total_wickets_taken = get_total_wickets_taken()


# Commit the changes and close the connection
conn.commit()
conn.close()