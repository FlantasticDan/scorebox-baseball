from flask import Flask, request, render_template
from flask.globals import g
from flask_socketio import SocketIO, emit

from manager import BaseballManager

VERSION = 'v.0.1 (03012021)'

MANAGER = None # type: BaseballManager

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/setup')
def setup():
    return render_template('setup.html', version=VERSION)

@app.route('/init', methods=['POST'])
def init():
    setup = request.form
    global MANAGER
    MANAGER = BaseballManager(setup['home_team'], setup['visitor_team'], setup['home_color'], setup['visitor_color'])
    socketio.emit('event-reset', MANAGER.export_game_state(), broadcast=True)
    return 'OK'

@app.route('/scorekeeper')
def scorekeeper():
    global MANAGER
    if MANAGER:
        return render_template('scorekeeper.html', state=MANAGER.export_game_state())

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
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('inning-mode-update')
def inning_mode_change(data):
    global MANAGER
    if MANAGER:
        MANAGER.set_inning_mode(data)
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('inning-update')
def inning_change(data):
    global MANAGER
    if MANAGER:
        MANAGER.set_inning(data)
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('base-update')
def base_change(json):
    global MANAGER
    if MANAGER:
        MANAGER.set_base(json['base'], json['state'])
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('base-reset')
def base_reset(data):
    global MANAGER
    if MANAGER:
        MANAGER.clear_bases()
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('out-update')
def out_change(data):
    global MANAGER
    if MANAGER:
        MANAGER.out(data)
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('out-reset')
def out_reset(data):
    global MANAGER
    if MANAGER:
        MANAGER.reset_outs()
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('strike-update')
def strike_change(data):
    global MANAGER
    if MANAGER:
        MANAGER.strike(data)
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('ball-update')
def ball_change(data):
    global MANAGER
    if MANAGER:
        MANAGER.ball(data)
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)

@socketio.on('count-reset')
def count_reset(data):
    global MANAGER
    if MANAGER:
        MANAGER.reset_count()
        return emit('event-reset', MANAGER.export_game_state(), broadcast=True)


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('icons/favicon.ico')

if __name__ == '__main__':
    socketio.run(app, port=5000)