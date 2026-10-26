import os
import re
import threading
import serial
from serial.tools import list_ports
import sqlite3
from flask import Flask, render_template, request, jsonify, Response
from add_item import SCHEMA

##### SETUP #####

PORT_NAME = "FT230X Basic UART"
matches = [p for p in list_ports.comports() if PORT_NAME in (p.description or "")]
if not matches:
    raise SystemExit(f"No serial port with '{PORT_NAME}' in its name found")
port = matches[0]
print(f"Using {port.device} - {port.description}")
ser = serial.Serial(port=port.device, baudrate=9600, timeout=1)

WEIGHT_RE = re.compile(rb'^\s*(-?\d+(?:\.\d+)?)\s*(kg|g)\s*$')

##### FUNCTIONS #####

def read_weight():
    raw = ser.readline().replace(b'\x00', b'')
    match = WEIGHT_RE.match(raw.strip(b'\r\n'))
    if not match:
        return None  # fragment, blank line or unstable ("?") reading
    value = float(match.group(1))
    return value * 1000 if match.group(2) == b'kg' else value


def get_db():
    conn = sqlite3.connect('kiosk.db')
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    return conn


def scale_loop():
    """Keep the latest stable weight (grams) in latest_weight."""
    global latest_weight
    while True:
        weight = read_weight()
        if weight is not None:
            latest_weight = weight


##### WEB APP #####

app = Flask(__name__)
latest_weight = None


@app.route('/')
def index():
    return render_template('kiosk.html')


@app.route('/api/weight')
def api_weight():
    return jsonify(weight=latest_weight)


@app.route('/api/items')
def api_items():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, name, category, price, weight_g, tolerance_g, stock "
            "FROM items ORDER BY category, name"
        ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route('/api/checkout', methods=['POST'])
def api_checkout():
    ids = request.get_json(force=True).get('ids', [])
    with get_db() as conn:
        for item_id in ids:
            conn.execute("UPDATE items SET stock = MAX(stock - 1, 0) WHERE id = ?", (item_id,))
    return jsonify(ok=True)


##### ADMIN #####

ADMIN_PASSWORD = os.environ.get('KIOSK_ADMIN_PASSWORD')  # unset = no login required


@app.before_request
def require_admin_login():
    if not ADMIN_PASSWORD:
        return
    if request.path.startswith('/admin') or request.path.startswith('/api/admin'):
        auth = request.authorization
        if not auth or auth.password != ADMIN_PASSWORD:
            return Response('Login required', 401, {'WWW-Authenticate': 'Basic realm="Kiosk admin"'})


def parse_item(data):
    """Validate an item payload, returning (fields, error)."""
    try:
        fields = {
            'name': str(data['name']).strip(),
            'category': (str(data.get('category') or '').strip() or None),
            'price': float(data['price']),
            'weight_g': float(data['weight_g']),
            'tolerance_g': float(data.get('tolerance_g', 5)),
            'stock': int(data.get('stock', 0)),
        }
    except (KeyError, TypeError, ValueError):
        return None, "Name, price and weight are required and must be valid numbers"
    if not fields['name']:
        return None, "Name is required"
    if fields['price'] < 0 or fields['weight_g'] <= 0 or fields['tolerance_g'] < 0 or fields['stock'] < 0:
        return None, "Price, tolerance and stock can't be negative, and weight must be above 0"
    return fields, None


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/api/admin/items', methods=['POST'])
def admin_create_item():
    fields, error = parse_item(request.get_json(force=True))
    if error:
        return jsonify(error=error), 400
    try:
        with get_db() as conn:
            cur = conn.execute(
                f"INSERT INTO items ({', '.join(fields)}) VALUES ({', '.join('?' * len(fields))})",
                tuple(fields.values()))
    except sqlite3.IntegrityError:
        return jsonify(error=f"An item named '{fields['name']}' already exists"), 409
    return jsonify(id=cur.lastrowid), 201


@app.route('/api/admin/items/<int:item_id>', methods=['PUT'])
def admin_update_item(item_id):
    fields, error = parse_item(request.get_json(force=True))
    if error:
        return jsonify(error=error), 400
    try:
        with get_db() as conn:
            cur = conn.execute(
                f"UPDATE items SET {', '.join(f'{k} = ?' for k in fields)} WHERE id = ?",
                (*fields.values(), item_id))
    except sqlite3.IntegrityError:
        return jsonify(error=f"An item named '{fields['name']}' already exists"), 409
    if cur.rowcount == 0:
        return jsonify(error="Item not found"), 404
    return jsonify(ok=True)


@app.route('/api/admin/items/<int:item_id>', methods=['DELETE'])
def admin_delete_item(item_id):
    with get_db() as conn:
        cur = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    if cur.rowcount == 0:
        return jsonify(error="Item not found"), 404
    return jsonify(ok=True)


if __name__ == '__main__':
    threading.Thread(target=scale_loop, daemon=True).start()
    app.run(host='127.0.0.1', port=5000)
