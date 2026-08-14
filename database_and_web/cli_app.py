import sqlite3
import os
db_path = os.path.join(os.path.dirname(__file__), "northwind.db")
con = sqlite3.connect(db_path)
con.row_factory = sqlite3.Row # allows row['name'] instead of row[1]
#con.set_trace_callback(print)

cur = con.cursor()

while True:
    print("1. Search customers")
    print("2. Create category")
    print("3. Show categories")
    print("4. Delete category")

    opt = int(input("? "))

    if opt == 1:
        q = input("Search for: ")
        q_res = cur.execute("SELECT CustomerID,CustomerName,Address FROM Customers WHERE CustomerName LIKE ?;", (f"%{q}%",))
        if q_res.rowcount == 0:
            print(f"No results found for '{q}'")
        else:
            for row in q_res.fetchall():
                print(f"[{row['CustomerID']}]: {row['CustomerName']} | {row['Address']}")
    elif opt == 2:
        catname = input("Category name: ")
        catdesc = input("Category description: ")
        cur.execute("INSERT INTO Categories (CategoryName, Description) VALUES (?, ?)", (catname, catdesc))
        con.commit() # Commit when changing data
        print(f"Category '{catname}' created.")
    elif opt == 3:
        res = cur.execute("SELECT * FROM Categories;")
        for row in res.fetchall():
            print(row['CategoryId'], row['CategoryName'], row['Description'])
    elif opt == 4:
        #list categories and then ask for id to delete
        res = cur.execute("SELECT * FROM Categories;")
        for row in res.fetchall():
            print(f"[{row['CategoryId']}]: {row['CategoryName']} | {row['Description']}")
        catid = int(input("Category ID to delete: "))
        cur.execute("DELETE FROM Categories WHERE CategoryId = ?", (catid,))
        con.commit()