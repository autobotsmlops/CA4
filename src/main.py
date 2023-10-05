from flask import Flask, request, jsonify, render_template
# import sqlite3 as sql
from todo import Todo as _Todo

app = Flask(__name__)

Todo = None

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

@app.route('/getTask/<name>', methods=['GET'])
def getTask(name):
    task = Todo.getTask(name)
    if task:
        return jsonify({'task': task.__dict__})
    return jsonify({'task': None})

@app.route('/deleteTask/<name>', methods=['DELETE'])
def deleteTask(name):
    result = Todo.deleteTask(name)
    return jsonify({'result': result})

@app.route('/updateTask/<name>', methods=['PUT'])
def updateTask(name):
    data = request.get_json()
    description = data['description']
    status = data['status']
    dueDate = data['dueDate']
    task = Todo.updateTask(name, description, status, dueDate)
    return jsonify({'task': task.__dict__})

@app.route('/searchTask/<name>', methods=['GET'])
def searchTask(name):
    tasks = Todo.searchTask(name)
    return jsonify({'tasks': [task.__dict__ for task in tasks]})

if __name__ == '__main__':

    Todo = _Todo()

    app.run(host='0.0.0.0', debug=True, port=5000)