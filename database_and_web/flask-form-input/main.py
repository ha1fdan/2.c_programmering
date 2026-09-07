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

if __name__ == '__main__':
    app.run(debug=True, port=5000)