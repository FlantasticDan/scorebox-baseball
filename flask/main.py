from flask import Flask, request, render_template
import flask
from flask_socketio import SocketIO, emit

VERSION = 'v.0.1 (02272021)'

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/setup')
def setup():
    return render_template('setup.html', version=VERSION)

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('icons/favicon.ico')

if __name__ == '__main__':
    socketio.run(app, port=5000)