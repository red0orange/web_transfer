from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Save all messages to this list
messages = []

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    # Save the message to the list
    messages.append(message)
    send(message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')

