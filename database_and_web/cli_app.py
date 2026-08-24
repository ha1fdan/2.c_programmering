import sqlite3
import os
from datetime import datetime
import prettytable
from InquirerPy import prompt,inquirer
db_path = os.path.join(os.path.dirname(__file__), "northwind.db")
con = sqlite3.connect(db_path)
con.row_factory = sqlite3.Row # allows row['name'] instead of row[1]
#con.set_trace_callback(print)

cur = con.cursor()

while True:
    print("1. Search customers")
    print("2. Search products")
    print("3. Create category")
    print("4. Show categories")
    print("5. Delete category")
    print("6. Create product")
    print("7. Delete product")
    print("8. Create order")
    print("0. Exit")

    opt = int(input("? "))

    if opt == 1:
        q = input("Search for: ")
        q_res = cur.execute("SELECT CustomerID,CustomerName,Address FROM Customers WHERE CustomerName LIKE ?;", (f"%{q}%",))
        table = prettytable.PrettyTable(["CustomerID", "Customer Name", "Address"])
        if q_res.rowcount == 0:
            print(f"No results found for '{q}'")
            table.add_row(["No results found", "", ""])
        else:
            for row in q_res.fetchall():
                table.add_row([row['CustomerID'], row['CustomerName'], row['Address']])
            print(table)
    elif opt == 2:
        q = input("Search for: ")
        q_res = cur.execute(
            """
            SELECT
                Products.ProductID,
                Products.ProductName,
                Products.Price,
                Categories.CategoryName,
                Suppliers.SupplierName,
                Suppliers.Address
            FROM Products
            JOIN Categories ON Products.CategoryID = Categories.CategoryID
            JOIN Suppliers ON Products.SupplierID = Suppliers.SupplierID
            WHERE Products.ProductName LIKE ?;
            """,
            (f"%{q}%",),
        )
        rows = q_res.fetchall()
        table = prettytable.PrettyTable(["ProductID", "Product", "Price", "Category", "Supplier", "Supplier Address"])
        if not rows:
            table.add_row(["No results found", "", "", "", "", ""])
            print(table)
        else:
            for row in rows:
                
                table.add_row([row['ProductID'], row['ProductName'], row['Price'], row['CategoryName'], row['SupplierName'], row['Address']])
            print(table)
    elif opt == 3:
        catname = input("Category name: ")
        catdesc = input("Category description: ")
        cur.execute("INSERT INTO Categories (CategoryName, Description) VALUES (?, ?)", (catname, catdesc))
        con.commit() # Commit when changing data
        print(f"Category '{catname}' created.")
    elif opt == 4:
        res = cur.execute("SELECT * FROM Categories;")
        for row in res.fetchall():
            print(row['CategoryId'], row['CategoryName'], row['Description'])
    elif opt == 5:
        #list categories and then ask for id to delete
        res = cur.execute("SELECT * FROM Categories;")
        for row in res.fetchall():
            print(f"[{row['CategoryId']}]: {row['CategoryName']} | {row['Description']}")
        catid = int(input("Category ID to delete: "))
        cur.execute("DELETE FROM Categories WHERE CategoryId = ?", (catid,))
        con.commit()
    
    elif opt == 6:
        #Create a new product (InquirerPy select category and supplier)
        product_name = input("Product name: ")
        product_price = float(input("Product price: "))
        #Select category
        categories = cur.execute("SELECT * FROM Categories;").fetchall()
        category_choices = [{"name": f"{row['CategoryId']}: {row['CategoryName']}", "value": row['CategoryId']} for row in categories]
        category_id = inquirer.select(message="Select category:", choices=category_choices).execute()
        #Select supplier
        suppliers = cur.execute("SELECT * FROM Suppliers;").fetchall()
        supplier_choices = [{"name": f"{row['SupplierId']}: {row['SupplierName']}", "value": row['SupplierId']} for row in suppliers]
        supplier_id = inquirer.select(message="Select supplier:", choices=supplier_choices).execute()
        cur.execute("INSERT INTO Products (ProductName, Price, CategoryID, SupplierID) VALUES (?, ?, ?, ?)", (product_name, product_price, category_id, supplier_id))
        con.commit()
    
    elif opt == 7:
        #Delete a product (InquirerPy select product)
        products = cur.execute("SELECT * FROM Products;").fetchall()
        product_choices = [{"name": f"{row['ProductId']}: {row['ProductName']}", "value": row['ProductId']} for row in products]
        product_id = inquirer.select(message="Select product to delete:", choices=product_choices).execute()
        cur.execute("DELETE FROM Products WHERE ProductId = ?", (product_id,))
        con.commit()
        
    elif opt == 8:
        # Avanceret: Oprette en ny ordre (kræver man kan vælge en kunde, vælge varer, vælge supplier osv. før man overhovedet kan indsætte en ordre).
        customers = cur.execute("SELECT * FROM Customers;").fetchall()
        customer_choices = [{"name": f"{row['CustomerId']}: {row['CustomerName']}", "value": row['CustomerId']} for row in customers]
        customer_id = inquirer.select(message="Select customer:", choices=customer_choices).execute()
        # Select employee
        employees = cur.execute("SELECT * FROM Employees;").fetchall()
        employee_choices = [{"name": f"{row['EmployeeId']}: {row['FirstName']} {row['LastName']}", "value": row['EmployeeId']} for row in employees]
        employee_id = inquirer.select(message="Select employee:", choices=employee_choices).execute()
        # Select shipper
        shippers = cur.execute("SELECT * FROM Shippers;").fetchall()
        shipper_choices = [{"name": f"{row['ShipperId']}: {row['ShipperName']}", "value": row['ShipperId']} for row in shippers]
        shipper_id = inquirer.select(message="Select shipper:", choices=shipper_choices).execute()
        # Select products (multiple)
        products = cur.execute("SELECT * FROM Products;").fetchall()
        product_choices = [{"name": f"{row['ProductId']}: {row['ProductName']}", "value": row['ProductId']} for row in products]
        product_ids = inquirer.checkbox(message="Select products:", choices=product_choices).execute()
        quantities = {}
        for product_id in product_ids:
            quantities[product_id] = int(input(f"Quantity for product {product_id}: "))
        # Insert order
        order_date = datetime.now().isoformat(sep=" ", timespec="seconds")
        cur.execute(
            "INSERT INTO Orders (CustomerId, EmployeeId, OrderDate, ShipperId) VALUES (?, ?, ?, ?)",
            (customer_id, employee_id, order_date, shipper_id),
        )
        order_id = cur.lastrowid
        for product_id in product_ids:
            cur.execute(
                "INSERT INTO OrderDetails (OrderId, ProductId, Quantity) VALUES (?, ?, ?)",
                (order_id, product_id, quantities[product_id]),
            )
        con.commit()
        print(f"Order created with ID: {order_id}")
        table = prettytable.PrettyTable(["OrderId", "CustomerId", "EmployeeId", "ShipperId", "OrderDate", "ProductIds"])
        table.add_row([order_id, customer_id, employee_id, shipper_id, order_date, ", ".join(f"{product_id} x{quantities[product_id]}" for product_id in product_ids)])
        print(table)
    elif opt == 0:
        import sys
        sys.exit(0)
    print("\n")