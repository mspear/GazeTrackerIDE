from flask import Flask
from flask_assets import Bundle, Environment

app = Flask(__name__)

bundles = { # Bundle our javascript files
    'home_js': Bundle(
        'webgazer.js',
        'jquery-3.3.1.js',
        output='gen/home.js',
        filters='jsmin',
    )
}

assets = Environment(app)
assets.register(bundles)

@app.route('/')
def hello_world():
    return "Hello World"


if __name__ == '__main__':
    app.run()
