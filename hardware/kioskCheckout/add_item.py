import argparse
import sqlite3
import sys

DB_PATH = 'kiosk.db'

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT    NOT NULL UNIQUE,
    category     TEXT,
    price        REAL    NOT NULL CHECK (price >= 0),   -- DKK
    weight_g     REAL    NOT NULL CHECK (weight_g > 0), -- expected weight of one item
    tolerance_g  REAL    NOT NULL DEFAULT 5,            -- allowed deviation when weighing
    stock        INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
)
"""


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(SCHEMA)
    return conn


def add_item(args):
    with connect() as conn:
        try:
            cur = conn.execute(
                "INSERT INTO items (name, category, price, weight_g, tolerance_g, stock) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (args.name, args.category, args.price, args.weight,
                 args.tolerance, args.stock),
            )
        except sqlite3.IntegrityError as e:
            sys.exit(f"Could not add item: {e}")
    print(f"Added #{cur.lastrowid}: {args.name} - {args.price:.2f} kr, "
          f"{args.weight:g} g (±{args.tolerance:g} g), stock {args.stock}")


def list_items(args):
    with connect() as conn:
        rows = conn.execute(
            "SELECT id, name, category, price, weight_g, tolerance_g, stock "
            "FROM items ORDER BY name"
        ).fetchall()
    if not rows:
        print("No items yet.")
        return
    print(f"{'ID':>3}  {'Name':<24} {'Category':<12} "
          f"{'Price':>8} {'Weight':>9} {'Tol':>6} {'Stock':>5}")
    for id_, name, category, price, weight, tol, stock in rows:
        print(f"{id_:>3}  {name:<24} {category or '-':<12} "
              f"{price:>7.2f}k {weight:>8g}g {tol:>5g}g {stock:>5}")


def update_item(args):
    fields = {
        'name': args.new_name,
        'category': args.category,
        'price': args.price,
        'weight_g': args.weight,
        'tolerance_g': args.tolerance,
        'stock': args.stock,
    }
    fields = {k: v for k, v in fields.items() if v is not None}
    if not fields:
        sys.exit("Nothing to update, pass at least one of --name --price --weight "
                 "--tolerance --stock --category")
    assignments = ", ".join(f"{k} = ?" for k in fields)
    with connect() as conn:
        try:
            cur = conn.execute(f"UPDATE items SET {assignments} WHERE name = ?",
                               (*fields.values(), args.name))
        except sqlite3.IntegrityError as e:
            sys.exit(f"Could not update item: {e}")
    if cur.rowcount == 0:
        sys.exit(f"No item named '{args.name}'")
    print(f"Updated {args.name}: " + ", ".join(f"{k}={v}" for k, v in fields.items()))


def delete_item(args):
    with connect() as conn:
        cur = conn.execute("DELETE FROM items WHERE name = ?", (args.name,))
    if cur.rowcount == 0:
        sys.exit(f"No item named '{args.name}'")
    print(f"Deleted {args.name}")


def positive(kind):
    def parse(value):
        n = kind(value)
        if n < 0:
            raise argparse.ArgumentTypeError("must not be negative")
        return n
    return parse


def main():
    parser = argparse.ArgumentParser(description="Manage kiosk items")
    sub = parser.add_subparsers(dest='command', required=True)

    add = sub.add_parser('add', help="add a new item")
    add.add_argument('name', help='e.g. "Coca-Cola 0.5L"')
    add.add_argument('price', type=positive(float), help="price in DKK")
    add.add_argument('weight', type=positive(float), help="weight of one item in grams")
    add.add_argument('--category', help='e.g. "drinks", "candy", "snacks"')
    add.add_argument('--tolerance', type=positive(float), default=5,
                     help="allowed weight deviation in grams (default 5)")
    add.add_argument('--stock', type=positive(int), default=0, help="units in stock (default 0)")
    add.set_defaults(func=add_item)

    up = sub.add_parser('update', help="change fields of an existing item")
    up.add_argument('name', help="current name of the item")
    up.add_argument('--name', dest='new_name', help="rename the item")
    up.add_argument('--price', type=positive(float), help="price in DKK")
    up.add_argument('--weight', type=positive(float), help="weight of one item in grams")
    up.add_argument('--tolerance', type=positive(float), help="allowed deviation in grams")
    up.add_argument('--stock', type=positive(int), help="units in stock")
    up.add_argument('--category')
    up.set_defaults(func=update_item)

    rm = sub.add_parser('delete', help="delete an item")
    rm.add_argument('name')
    rm.set_defaults(func=delete_item)

    ls = sub.add_parser('list', help="list all items")
    ls.set_defaults(func=list_items)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
