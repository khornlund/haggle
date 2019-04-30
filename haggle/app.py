from uuid import uuid4

from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_socketio import SocketIO

from session import SessionManager

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
        return redirect(url_for('buyer_session'))
    elif role.lower() == 'seller':
        return redirect(url_for('seller_session'))


@app.route('/session/buyer')
def buyer_session():
    resp = make_response(render_template('session.html'))
    resp.set_cookie('UUID', sm.new_buyer())
    return resp


@app.route('/session/seller')
def seller_session():
    resp = make_response(render_template('session.html'))
    resp.set_cookie('UUID', sm.new_seller())
    return resp


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
    socketio.run(app, debug=True)
