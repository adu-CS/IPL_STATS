from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Home Page route
@app.route("/")
def home():
    return render_template("home.html")

# Route to form used to add a new player to the database
@app.route("/enternew")
def enternew():
    return render_template("player.html")

@app.route("/Teams")
def Teams():
    return render_template("teams.html")

@app.route("/tnmt")
def tnmt():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    # Fetch the tournament name from the database
    cursor.execute("SELECT tournament_id, tournament_name FROM Tournaments")
    tournament_name = cursor.fetchall()

    conn.close()
    return render_template("tnmt.html", tournament_name=tournament_name)

@app.route("/tournament_details")
def tournament_details():
    return render_template("all_tourney.html")

@app.route("/score")
def score():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(runs_scored) FROM ballbyball")
    total_runs = cursor.fetchone()[0]

    # Calculate the total wickets
    cursor.execute("SELECT COUNT(*) FROM ballbyball WHERE wicket_type !='NONE' AND wicket_type != ''")
    total_wickets = cursor.fetchone()[0]

    conn.close()

    return render_template("score.html", total_runs=total_runs, total_wickets=total_wickets)


#create tournament
@app.route("/crt_tnmt")
def crt_tnmt():
    return render_template("create_tnmt.html")

@app.route("/crt_match")
def crt_match():
    return render_template("crt_match.html")

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

        return redirect(url_for('matches'))
    except Exception as e:
        return f"An error occurred: {e}"


@app.route("/matches")
def matches():
    con = sqlite3.connect("database.sqlite")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM Matches")

    rows = cur.fetchall()
    con.close()
    # Logic to retrieve matches data from the database goes here
    return render_template("matches.html", matches=rows)  # Render the matches page template


@app.route('/conduct')
def conduct():
    return render_template("ballbyball.html")

@app.route("/submit_ballbyball", methods=["POST"])
def submit_ballbyball():
    if request.method == "POST":
        try:
            # Extract data from the form
            match_id = request.form["match_id"]
            inning = request.form["inning"]
            over_number = request.form["over_number"]
            ball_number = request.form["ball_number"]
            batter_id = request.form["batter_id"]
            bowler_id = request.form["bowler_id"]
            runs_scored = request.form["runs_scored"]
            extras = request.form["extras"]
            wicket_type = request.form["wicket_type"]
            fielder_id = request.form.get("fielder_id", None)

            # Connect to the SQLite database
            conn = sqlite3.connect('database.sqlite')
            cursor = conn.cursor()

            # Insert data into ballbyball table
            cursor.execute("""
                INSERT INTO ballbyball (match_id, inning, over_number, ball_number, batter_id, bowler_id, runs_scored, extras, wicket_type, fielder_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (match_id, inning, over_number, ball_number, batter_id, bowler_id, runs_scored, extras, wicket_type, fielder_id))

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            # Redirect to a success page or wherever you want
            return redirect(url_for('success'))
        except Exception as e:
            # Handle errors
            return f"An error occurred: {e}"



@app.route("/success")
def success():
    return "Data submitted successfully!"

    

@app.route('/newrectnmt', methods=['POST'])
def newrectnmt():
    if request.method == 'POST':
        try:
            # Extract form data
            tournament_name = request.form['tournament_name']
            tournament_id = request.form['tournament_id']
            year = request.form['year']
            location = request.form['location']
            organizer_name = request.form['organizer_name']
            organizer_id = request.form['organizer_id']
            contact_email = request.form['contact_email']

            # Connect to SQLite database
            conn = sqlite3.connect('database.sqlite')
            if conn is not None:
                # Insert data into 'Tournaments' table
                with conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO Tournaments (tournament_id, tournament_name, year, location, organizer_id, organizer_name, contact_email) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                   (tournament_id, tournament_name, year, location, organizer_id, organizer_name, contact_email))
                print("Data inserted successfully")
            else:
                print("Connection to SQLite database failed")

            # Return a response indicating success
            return "Tournament created successfully"
        except Exception as e:
            print(f"Error inserting data into SQLite database: {e}")
            return "An error occurred while creating the tournament"

              


# Route to add a new record (INSERT) player data to the database
@app.route("/addrec", methods=['POST'])
def addrec():
    if request.method == 'POST':
        try:
            ply_id=request.form['ply_id']
            name = request.form['name']
            runs = request.form['runs']
            avg = request.form['avg']
            sr = request.form['sr']
            team=request.form['team']

            with sqlite3.connect('database.sqlite') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Players (ply_id, name, runs, avg, sr, team) VALUES (?, ?, ?, ?, ?, ?)", (ply_id, name, runs, avg, sr, team))
                con.commit()
                msg = "Record successfully added to database"
        except:
            con.rollback()
            msg = "Error in the INSERT"

        finally:
            con.close()
            return render_template('result.html', msg=msg)

# Route to SELECT all data from the Players table and display in a table
@app.route('/list')
def list():
    con = sqlite3.connect("database.sqlite")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM Players")

    rows = cur.fetchall()
    con.close()
    return render_template("list.html", rows=rows)

# Route that will SELECT a specific row in the database then load an Edit form 
@app.route("/edit", methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        try:
            id = request.form['id']
            with sqlite3.connect("database.sqlite") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("SELECT rowid, * FROM Players WHERE rowid = ?", (id,))
                rows = cur.fetchall()
        except:
            rows = None
        return render_template("edit.html", rows=rows)

# Route used to execute the UPDATE statement on a specific record in the database
@app.route("/editrec", methods=['POST'])
def editrec():
    if request.method == 'POST':
        try:
            rowid = request.form['rowid']
            ply_id=request.form['ply_id']
            name = request.form['name']
            runs = request.form['runs']
            avg = request.form['avg']
            sr = request.form['sr']
            team=request.form['team']

            with sqlite3.connect('database.sqlite') as con:
                cur = con.cursor()
                cur.execute("UPDATE Players SET ply_id=?, name=?, runs=?, avg=?, sr=?, team=? WHERE rowid=?", (ply_id, name, runs, avg, sr, team, rowid))
                con.commit()
                msg = "Record successfully edited in the database"
        except:
            con.rollback()
            msg = "Error in the Edit"

        finally:
            con.close()
            return render_template('result.html', msg=msg)

# Route used to DELETE a specific record in the database    
@app.route("/delete", methods=['POST'])
def delete():
    if request.method == 'POST':
        try:
            rowid = request.form['id']
            with sqlite3.connect('database.sqlite') as con:
                cur = con.cursor()
                cur.execute("DELETE FROM Players WHERE rowid=?", (rowid,))
                con.commit()
                msg = "Record successfully deleted from the database"
        except:
            con.rollback()
            msg = "Error in the DELETE"

        finally:
            con.close()
            return render_template('result.html', msg=msg)

if __name__ == "__main__":
    app.run(debug=True)