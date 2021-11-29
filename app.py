from sys import modules
import uuid
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from database import Database
from uuid import uuid4

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
database = Database()


@app.route("/")
def index():
    moodboards = database.query('SELECT * FROM `moodboard`')
    return render_template('index.html', **locals())

@app.route("/features")
def features():
    return jsonify(database.query('SELECT * FROM `marktplaats_images`'))    

@socketio.on('request-recommendations')
def recommend(moodboard):
    #Tom do stuff to return reqs
    pass

@socketio.on('create-new-moodboard')
def create_new_moodboard(moodboard):
    query_list = []

    moodboard_id = uuid4()
    query_list.append(f"INSERT INTO `moodboard` VALUES({moodboard_id}, {moodboard['name']})")
    
    for item in moodboard["items"]:
        query_list.append(f"INSERT INTO `image` VALUES({moodboard_id}, {uuid4()},{item})")
    
    database.execute(query_list)



@socketio.on('connect')
def connect():
    print('user connected')

if __name__ == '__main__':
    socketio.run(app)
    app.run(host='0.0.0.0', port=5000, debug=True)