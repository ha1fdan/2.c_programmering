from flask import Flask, render_template, request, g
import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), "flask-app.db")

app = Flask(__name__)

# https://flask.palletsprojects.com/en/stable/patterns/sqlite3/
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
# Prepare the database
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        db.commit()

# Flask Routes
@app.route('/')
def root():
    #return "I'm root!"
    return render_template('root.html')

@app.route('/form/get')
def get():
    name = request.args.get('name')
    email = request.args.get('email')
    return render_template('get.html', name=name, email=email)

@app.route('/form/post', methods=['GET', 'POST'])
def post():
    message = "Please login"
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Username: {username}, Password: {password}")
        
        if username == 'ostebob' and password == '1234!':
            message = "secret shit"
        else:
            message = "wrong combination of username and password"
    return render_template('post.html', message=message)

@app.route('/form/post2', methods=['GET'])
def post2():
    return render_template('post2.html')

@app.route('/whatever/process', methods=['POST'])
def process():
    username = request.form['username']
    password = request.form['password']
    print(f"Processing username: {username}")
    print(f"Processing password: {password}")
    if username == 'ostebob' and password == '1234!':
        print("Access granted")
    else:
        print("Access denied")
    return "Processing complete"

@app.route('/message-board', methods=['GET', 'POST'])
def message_board():
    # Message board with SQLite database
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        message_text = request.form['message']
        #print(username, message_text)
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO messages (username, message) VALUES (?, ?)', (username, message_text))
        db.commit()
        message = "Message posted!"
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT username, message FROM messages ORDER BY id DESC LIMIT 10')
    messages = cursor.fetchall()
    return render_template('post3.html', message=message, messages=messages)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)