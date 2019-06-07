from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_socketio import SocketIO

from haggle.session import SessionManager

app = Flask(__name__)
app.config['SECRET_KEY'] = b';M\x7f\x9b\x83^b\x84\xb3\x1f/\xe0d\x01\xb4?J\xc4!\x10'
socketio = SocketIO(app)


# -- resources --

sm = SessionManager()


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
        ssn = sm.new_buyer()
        resp = make_response(render_template('session_buy.html', data=ssn.data))
        resp.set_cookie('UUID', ssn.uuid)
        return resp

    uuid = request.cookies.get('UUID')
    msg = request.form['message']
    ssn = sm.buyers[uuid]
    resp = ssn.receive(msg)
    return render_template('session_buy.html', data=ssn.data)


@app.route('/session/seller', methods=['GET', 'POST'])
def session_seller():
    if request.method != 'POST':
        ssn = sm.new_seller()
        resp = make_response(render_template('session_sell.html', data=ssn.data))
        resp.set_cookie('UUID', ssn.uuid)
        return resp

    uuid = request.cookies.get('UUID')
    msg = request.form['message']
    ssn = sm.sellers[uuid]
    resp = ssn.receive(msg)
    return render_template('session_sell.html', data=ssn.data)


# -- handlers --

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    uuid = request.cookies.get('UUID')
    print(f'Received my event {json} from session {uuid}')
    socketio.emit('my response', json, callback=message_received)


# -- util --

def message_received(methods=['GET', 'POST']):
    print('Message received!')


if __name__ == '__main__':
    socketio.run(host='0.0.0.0', port=5000, debug=True)
