from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template('index.html')

@socketio.on('connection')
def connection():
    print('user connected')

if __name__ == '__main__':
    socketio.run(app)
    app.run(host='0.0.0.0', port=5000, debug=True)