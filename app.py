import subprocess

from flask import Flask, render_template, request, url_for
from flask_assets import Bundle, Environment
from flask_codemirror import CodeMirror
from flask_socketio import SocketIO, emit

CODEMIRROR_LANGUAGES = ['python', 'html']

app = Flask(__name__)

app.config.from_object(__name__)
codemirror = CodeMirror(app)
bundles = {  # Bundle our javascript files
    'home_js': Bundle(
        'js/webgazer.js',
        'js/jquery-3.3.1.js',
        output='gen/home.js',
        filters='jsmin',
    )
}

socketio = SocketIO(app)
assets = Environment(app)
assets.register(bundles)

@socketio.on('sendDataHost')
def hostReflect(data):
    emit('receiveDataHost', data, broadcast=True)

@socketio.on('sendDataWatcher')
def watcherReflect(data):
    emit('receiveDataWatcher', data, broadcast=True)


def exec_code(code):
    proc = subprocess.Popen(
        ['python', '-c', code],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    acc = ''
    for line in iter(proc.stdout.readline, b''):
        acc += line.decode()
    return acc

@app.route('/ajax/runCode', methods=['POST'])
def runcode():
    result = exec_code(request.form['data'])
    return result


@app.route('/host', methods=['GET'])
def host():
    filename = request.args.get('filename')
    data = ''

    if filename:
        import os
        with open(os.path.join(app.static_folder, f'py/{filename}.py'), 'r') as f:
            data = f.read()
    print(data)
    return render_template('host.html', data=data)


@app.route('/watcher', methods=['GET'])
def watch():
    return render_template('watcher.html')


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000,  keyfile='key.pem', certfile='cert.pem')
