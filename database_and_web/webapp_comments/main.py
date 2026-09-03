from flask import Flask, g, request, render_template, redirect, url_for
import sqlite3
import os

import prettytable

db_path = os.path.join(os.path.dirname(__file__), "messages.db")

app = Flask(__name__)

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()

with app.app_context():
    db = sqlite3.connect(db_path)
    db.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, name TEXT, message TEXT);")
    db.commit()
    db.close()

@app.route("/")
def index():
    messages = get_db().execute("SELECT * FROM messages ORDER BY id DESC LIMIT 50;").fetchall()
    table = prettytable.PrettyTable(["ID", "Name", "Message"])
    for row in messages:
        table.add_row([row['id'], row['name'], row['message']])
    return render_template("index.html", table=table.get_string())

@app.route("/add", methods=["POST"])
def add_message():
    name = request.form["name"]
    message = request.form["message"]
    db = get_db()
    db.execute("INSERT INTO messages (name, message) VALUES (?, ?);", (name, message))
    db.commit()
    return redirect(url_for("index", _anchor="messages"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)