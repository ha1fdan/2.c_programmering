# https://docs.python.org/3/library/sqlite3.html#tutorialI
import sqlite3
con = sqlite3.connect("whatever.db") # Created if it does not exist
con.row_factory = sqlite3.Row # allows row['name'] instead of row[1]
#con.set_trace_callback(print)

con.execute("CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY, message TEXT, name TEXT);")

while True:
    name= input("Name:")
    msg = input("Message:")

    con.execute("INSERT INTO messages (message, name) VALUES (?,?)", (msg,name))
    con.commit()

    # Display all messages
    res = con.execute("SELECT * FROM messages")
    msgs = res.fetchall()
    for m in msgs:
        print(f"# {m['name']} says {m['message']}\n")





        





