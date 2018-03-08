from flask import Flask
from wtforms import form
from wtforms.fields import SubmitField
from flask.ext.codemirror import CodeMirror
from flask.ext.codemirror.fields import CodeMirrorField
from flask_assets import Bundle, Environment

class MyFrom(form):
    source_code = CodeMirrorField(language='python3', config={'lineNumbers': True})
    submit = SubmitField('Submit')

CODEMIRROR_LANGUAGES = ['python3', 'html']
app = Flask(__name__)

app.config.from_object(__name__)
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
