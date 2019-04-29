from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO


app = Flask(__name__)
socketio = SocketIO(app)


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
    return render_template('session.html')


@app.route('/session/seller')
def seller_session():
    return render_template('session.html')


# -- handlers --

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print(f'Received my event: {json}')
    socketio.emit('my response', json, callback=message_received)


# -- util --

def message_received(methods=['GET', 'POST']):
    print('Message received!')


if __name__ == '__main__':
    socketio.run(app, debug=True)
