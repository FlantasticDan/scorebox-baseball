from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit

from manager import BaseballManager

VERSION = 'v.0.1 (02282021)'

MANAGER = None # type: BaseballManager

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/setup')
def setup():
    return render_template('setup.html', version=VERSION)

@app.route('/init', methods=['POST'])
def init():
    setup = request.form
    MANAGER = BaseballManager(setup['home_team'], setup['visitor_team'], setup['home_color'], setup['visitor_color'])
    return 'OK'

@app.route('/scorekeeper')
def scorekeeper():
    return render_template('scorekeeper.html')

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('icons/favicon.ico')

if __name__ == '__main__':
    socketio.run(app, port=5000)