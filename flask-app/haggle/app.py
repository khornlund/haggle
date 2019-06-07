from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_socketio import SocketIO

from haggle.session import SessionManager
from haggle.logger import setup_logging, setup_logger

app = Flask(__name__)
app.config['SECRET_KEY'] = b';M\x7f\x9b\x83^b\x84\xb3\x1f/\xe0d\x01\xb4?J\xc4!\x10'
socketio = SocketIO(app)
logger = setup_logger('haggle-webapp')


# -- routes --

@app.route('/')
def default():
    return redirect(url_for('splash'))


@app.route('/splash', methods=['GET', 'POST'])
def splash():
    if request.method != 'POST':
        return render_template('splash.html')

    role = request.form['role_btn']
    if role.lower() == 'buyer':
        return redirect(url_for('session_buyer'))
    elif role.lower() == 'seller':
        return redirect(url_for('session_seller'))


@app.route('/session/buyer', methods=['GET', 'POST'])
def session_buyer():
    if request.method != 'POST':
        ssn = SessionManager().new_buyer()
        resp = make_response(render_template('session_buy.html', data=ssn.data))
        resp.set_cookie('UUID', ssn.uuid)
        return resp

    uuid = request.cookies.get('UUID')
    msg = request.form['message']
    ssn = SessionManager().buyers[uuid]
    resp = ssn.receive(msg)
    return render_template('session_buy.html', data=ssn.data)


@app.route('/session/seller', methods=['GET', 'POST'])
def session_seller():
    if request.method != 'POST':
        ssn = SessionManager().new_seller()
        resp = make_response(render_template('session_sell.html', data=ssn.data))
        resp.set_cookie('UUID', ssn.uuid)
        return resp

    uuid = request.cookies.get('UUID')
    msg = request.form['message']
    ssn = SessionManager().sellers[uuid]
    resp = ssn.receive(msg)
    return render_template('session_sell.html', data=ssn.data)


# -- handlers --

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    uuid = request.cookies.get('UUID')
    logger.info(f'Received my event {json} from session {uuid}')
    socketio.emit('my response', json, callback=message_received)


# -- util --

def message_received(methods=['GET', 'POST']):
    logger.info('Message received!')


# -- top level entry point --

def main(host, port, db_host, debug):
    setup_logging()
    sm = SessionManager()
    sm.set_db_host(db_host)  # set property on singleton
    socketio.run(app, host=host, port=port, debug=True)
