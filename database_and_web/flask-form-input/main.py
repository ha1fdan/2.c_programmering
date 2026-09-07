from flask import Flask, render_template, request

app = Flask(__name__)


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
    return "Processing complete"

if __name__ == '__main__':
    app.run(debug=True, port=5000)