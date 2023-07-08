from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
limiter = Limiter(app)
auth = HTTPBasicAuth()

# Create a dictionary to store user credentials. In a real-world application, this could be a database.
users = {
    "red0orange": generate_password_hash("jump1047235544")
}

# Save all messages to this list
messages = []

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/')
@limiter.limit("10000/day;1000/hour;100/minute")
@auth.login_required
def index():
    return render_template('index.html', messages=messages)

@limiter.limit("10000/day;1000/hour;100/minute")
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    # Save the message to the list
    id = str(len(messages))
    messages.append({'id': id, 'text': message})
    send({'id': id, 'text': message}, broadcast=True)

@socketio.on('delete')
@limiter.limit("10000/day;1000/hour;100/minute")
def handle_delete(id):
    # Remove the message with the given id
    messages[:] = [m for m in messages if m['id'] != id]
    send({'delete': id}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')

