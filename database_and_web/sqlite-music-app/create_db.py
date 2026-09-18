import sqlite3
import os.path
import sys

if os.path.exists("music.db"):
    print("music.db already exists, delete manually")
    sys.exit()

db = sqlite3.connect("music.db")

with open("music.sql", "r") as f:
    db.executescript(f.read())
    db.commit()
