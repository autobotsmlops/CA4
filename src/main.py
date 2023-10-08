import os
from flask import Flask, request, jsonify, render_template
from todo import Todo as _Todo

import mysql.connector

app = Flask(__name__)

Todo = None


def connect_to_db():
    if os.environ.get('ENV') is None:
        os.environ['ENV'] = 'local'

    if os.environ.get('ENV') == 'container':
        dbHost = os.environ.get('DB_HOST')

    if os.environ.get('ENV') == 'local':
        dbHost = 'localhost'
    
    return mysql.connector.connect(
        host=dbHost,
        port=3306,
        user="root",
        password="root",
        database="TODO"
    )

db = connect_to_db()
Todo = _Todo(db)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/addTask', methods=['POST'])
def addTask():
    data = request.get_json()
    name = data['name']
    description = data['description']
    dueDate = data['dueDate']
    task = Todo.addTask(name, description, dueDate)
    return jsonify({'task': task.__dict__})

@app.route('/getTasks', methods=['GET'])
def getTasks():
    tasks = Todo.getTasks()
    return jsonify({'tasks': [task.__dict__ for task in tasks]})

@app.route('/deleteTask/<id>', methods=['DELETE'])
def deleteTask(id):
    result = Todo.deleteTask(id)
    return jsonify({'result': result})

@app.route('/updateTask/<id>', methods=['PUT'])
def updateTask(id):
    data = request.get_json()
    name = data['name']
    description = data['description']
    status = data['status']
    dueDate = data['dueDate']
    task = Todo.updateTask(id, name, description, status, dueDate)
    if not task:
        return jsonify({'task': None})

    return jsonify({'task': task.__dict__})

@app.route('/searchTask/<name>', methods=['GET'])
def searchTask(name):
    if name == '':
        tasks = Todo.getTasks()
    else:
        tasks = Todo.searchTask(name)
    return jsonify({'tasks': [task.__dict__ for task in tasks]})

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True, port=5000)

    # Close the cursor and the database connection when done
    Todo.db.cursor.close()
    Todo.db.close()