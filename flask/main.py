import os
import subprocess

from flask import Flask, request, render_template
from flask.globals import g
from flask_socketio import SocketIO, emit

from manager import BaseballManager
import bundle

VERSION = 'v.0.1 (03022021)'

MANAGER = None # type: BaseballManager

LOCALKEY = 'debug'
OVERLAY_PATH = None
OVERLAY_PROCESS = None

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/setup')
def setup():
    global LOCALKEY
    if request.args['key'] == LOCALKEY:
        return render_template('setup.html', version=VERSION)
    else:
        return

@app.route('/init', methods=['POST'])
def init():
    setup = request.form
    global MANAGER
    global OVERLAY_PATH
    global OVERLAY_PROCESS
    global LOCALKEY
    if request.args['key'] == LOCALKEY:
        MANAGER = BaseballManager(setup['home_team'], setup['visitor_team'], setup['home_color'], setup['visitor_color'])
        OVERLAY_PROCESS = subprocess.Popen([OVERLAY_PATH, '-monitor', '2', '-screen-fullscreen', '1'])
        socketio.emit('event-reset', MANAGER.export_game_state(), broadcast=True)
        MANAGER.update_overlay()
        return 'OK'
    else:
        return

@app.route('/scorekeeper')
def scorekeeper():
    global MANAGER
    if MANAGER:
        return render_template('scorekeeper.html', state=MANAGER.export_game_state())

@app.route('/admin')
def admin():
    global MANAGER
    global LOCALKEY
    if request.args['key'] == LOCALKEY and MANAGER:
        return render_template('admin.html', version=VERSION, state=MANAGER.export_game_state())
    else:
        return

@socketio.on('event-request')
def update(data):
    global MANAGER
    if MANAGER:
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('score-update')
def score_change(json):
    global MANAGER
    if MANAGER:
        MANAGER.adjust_score(json['team'], json['score'])
        MANAGER.update_overlay()
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('inning-mode-update')
def inning_mode_change(data):
    global MANAGER
    if MANAGER:
        MANAGER.set_inning_mode(data)
        MANAGER.update_overlay()
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('inning-update')
def inning_change(data):
    global MANAGER
    if MANAGER:
        MANAGER.set_inning(data)
        MANAGER.update_overlay()
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('base-update')
def base_change(json):
    global MANAGER
    if MANAGER:
        MANAGER.set_base(json['base'], json['state'])
        MANAGER.update_overlay()
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('base-reset')
def base_reset(data):
    global MANAGER
    if MANAGER:
        MANAGER.clear_bases()
        MANAGER.update_overlay()
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('out-update')
def out_change(data):
    global MANAGER
    if MANAGER:
        MANAGER.out(data)
        MANAGER.update_overlay()
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('out-reset')
def out_reset(data):
    global MANAGER
    if MANAGER:
        MANAGER.reset_outs()
        MANAGER.update_overlay()
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('strike-update')
def strike_change(data):
    global MANAGER
    if MANAGER:
        MANAGER.strike(data)
        MANAGER.update_overlay()
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('ball-update')
def ball_change(data):
    global MANAGER
    if MANAGER:
        MANAGER.ball(data)
        MANAGER.update_overlay()
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('count-reset')
def count_reset(data):
    global MANAGER
    if MANAGER:
        MANAGER.reset_count()
        MANAGER.update_overlay()
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('icons/favicon.ico')

@app.route('/terminate')
def terminate():
    global OVERLAY_PROCESS
    global LOCALKEY
    if request.args['key'] == LOCALKEY:
        if OVERLAY_PROCESS:
            OVERLAY_PROCESS.kill()
        os.system("taskkill /F /PID " + str(os.getpid()))

if __name__ == '__main__':
    LOCALKEY, port, OVERLAY_PATH = bundle.setup(app)
    socketio.run(app, port=port)