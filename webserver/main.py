from flask import Flask, jsonify, render_template, render_template_string
from logging import DEBUG, Logger, basicConfig

logger=Logger(__name__)
basicConfig(level=DEBUG)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)