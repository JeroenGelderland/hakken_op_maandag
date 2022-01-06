from sys import modules
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from database import Database
import uuid
from uuid import uuid4
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
database = Database()


@app.route('/')
def index():
    moodboards = database.query('SELECT * FROM `moodboard`')
    return render_template('index.html', **locals())

@app.route('/features')
def features():
    return jsonify(database.query('SELECT * FROM `marktplaats_images`'))    

@socketio.on('request-recommendations')
def recommend(moodboard_id):
    results = database.query(f"SELECT * FROM `image` WHERE `board` = {moodboard_id}")

    images = []

    for image in results:
        images.append(image['image'])

    data = { 'images': images }

    requests.post('http://192.168.1.97:5000', json = data) # Tom's ding
    pass

@socketio.on('create-new-moodboard')
def create_new_moodboard(moodboard):
    query_list = []

    moodboard_id = uuid4()
    query_list.append(f"INSERT INTO `moodboard` VALUES({moodboard_id}, {moodboard['name']})")
    
    for file in moodboard['files']:
        query_list.append(f"INSERT INTO `image` VALUES({moodboard_id}, {uuid4()}, {file})")
    
    database.execute(query_list)
    emit('new-moodboard-confirmed', { 'id': moodboard_id, 'name': moodboard['name'] })

@socketio.on('connect')
def connect():
    print('user connected')

if __name__ == '__main__':
    socketio.run(app)
    app.run(host = '0.0.0.0', port = 5000, debug = True)
