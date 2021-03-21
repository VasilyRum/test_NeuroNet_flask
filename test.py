from flask import Flask
from blueprint import bp

app = Flask(__name__)
app.register_blueprint(bp)


@app.route('/')
def hello():
    return 'Hello, World'