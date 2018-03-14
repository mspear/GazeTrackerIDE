from flask import Flask, render_template, request
from wtforms import Form
from wtforms.fields import SubmitField
from flask_codemirror import CodeMirror
from flask_codemirror.fields import CodeMirrorField
from flask_assets import Bundle, Environment
from flask_socketio import SocketIO, join_room, send

import subprocess


class MyForm(Form):
    source_code = CodeMirrorField(language='python', config={'lineNumbers': True})
    submit = SubmitField('Submit')




CODEMIRROR_LANGUAGES = ['python', 'html']

app = Flask(__name__)

app.config.from_object(__name__)
codemirror = CodeMirror(app)
bundles = {  # Bundle our javascript files
    'home_js': Bundle(
        'webgazer.js',
        'jquery-3.3.1.js',
        output='gen/home.js',
        filters='jsmin',
    )
}

socketio = SocketIO(app)
assets = Environment(app)
assets.register(bundles)


@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    print("someone joined!")


def exec_code(code):
    proc = subprocess.Popen(
        ['python', '-c', code],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    for line in iter(proc.stdout.readline, b''):
        yield line.decode().rstrip() + '\n'


@app.route('/host', methods=['GET', 'POST'])
def host():
    form = MyForm(request.form)
    if request.method == 'POST' and form.validate():
        text = form.source_code.data
    else:
        text = ''

    return render_template('host.html', form=form, postback=exec_code(text) if text else '')


@app.route('/watcher', methods=['GET'])
def watch():
    return render_template('watcher.html')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = MyForm(request.form)
    if request.method == 'POST' and form.validate():
        text = form.source_code.data
    else:
        text = ''

    return render_template('index.html', form=form, postback=exec_code(text) if text else '')


if __name__ == '__main__':
    socketio.run(app)
