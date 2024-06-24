from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Route to display the form to create a new match
@app.route("/crt_match", methods=["GET"])
def create_match_form():
    return render_template("crt_match.html")

# Route to handle the form submission and create a new match
@app.route("/crt_match", methods=["POST"])
def create_match():
    try:
        # Extract form data
        tournament_id = request.form['tournament_id']
        team1_id = request.form['team1_id']
        team2_id = request.form['team2_id']
        match_date = request.form['match_date']
        venue = request.form['venue']
        result = request.form.get('result', None)
        winning_team_id = request.form.get('winning_team_id', None)
        losing_team_id = request.form.get('losing_team_id', None)

        # Connect to SQLite database
        conn = sqlite3.connect('database.sqlite')
        cursor = conn.cursor()

        # Insert data into Matches table
        cursor.execute("""
            INSERT INTO Matches (tournament_id, team1_id, team2_id, match_date, venue, result, winning_team_id, losing_team_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (tournament_id, team1_id, team2_id, match_date, venue, result, winning_team_id, losing_team_id))

        conn.commit()
        conn.close()

        return redirect(url_for('create_match_form'))
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    app.run(debug=True)
