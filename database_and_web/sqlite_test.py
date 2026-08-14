# https://docs.python.org/3/library/sqlite3.html#tutorialI
import sqlite3
import os
db_path = os.path.join(os.path.dirname(__file__), "northwind.db")
con = sqlite3.connect(db_path)
con.row_factory = sqlite3.Row # allows row['name'] instead of row[1]
con.set_trace_callback(print)

cur = con.cursor()


# Fetch all
name = "%mar%"
res = cur.execute("SELECT * FROM Customers WHERE CustomerName LIKE ?;", (name,) )
for row in res.fetchall():
    print(row.keys())

exit()
# Fetch one
res = cur.execute("SELECT * FROM Customers WHERE CustomerID=1;")
row = res.fetchone()
print("fetchone():", row['CustomerId'], row['CustomerName'])


# Insert
catname = "Electronics"
catdesc = "Computers, phones, fridges, etc."
cur.execute("INSERT INTO Categories (CategoryName, Description) VALUES (?, ?)", (catname, catdesc))
con.commit() # Commit when changing data

# Fetch all
print("## Categories")
res = cur.execute("SELECT * FROM Categories;")
for row in res.fetchall():
    print(row['CategoryId'], row['CategoryName'], row['Description'])









