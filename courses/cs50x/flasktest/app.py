from cs50 import SQL
from flask import Flask, render_template, request

app = Flask(__name__)

db = SQL("sqlite:///flasktest.db")



SPORTS = [
    "Basketball",
    "Soccer",
    "Baseball",
]

@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)

@app.route("/register", methods=["POST"])
def register():

    name = request.form.get("name")
    if not name:
        return render_template("error.html", message="Missing name")
    sport = request.form.get("sport")
    if not sport:
        return render_template("error.html", message="Missing sport")
    if sport not in SPORTS:
        return render_template("error.html", message="Invalid sport")

    db.execute("INSERT INTO people (name, sport) VALUES (?, ?)", name, sport)


    if not request.form.get("name") or request.form.get("sport") not in SPORTS:
        return render_template("failure.html")
    return render_template("success.html")

@app.route("/people")
def people():
    people = db.execute("SELECT name, sport FROM people")
    return render_template("people.html", people=people)

if __name__ == "__main__":
    app.run(debug=False)