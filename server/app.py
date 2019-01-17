import os
import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

TODO = [
    {
        'id': uuid.uuid4().hex,
        'todo': 'todo',
        'assignee': 'assignee',
        'done': True,
    }
]


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/TODO', methods=['GET', 'POST'])
def all_TODO():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        TODO.append({
            'id': uuid.uuid4().hex,
            'todo': post_data.get('todo'),
            'assignee': post_data.get('assignee'),
            'done': post_data.get('done'),
        })
        response_object['message'] = 'todo added!'
    else:
        response_object['TODO'] = TODO
    return jsonify(response_object)


@app.route('/TODO/<todo_id>', methods=['GET', 'PUT', 'DELETE'])
def single_todo(todo_id):
    response_object = {'status': 'success'}
    if request.method == 'GET':
        # TODO: refactor to a lambda and filter
        return_todo = ''
        for todo in TODO:
            if todo['id'] == todo_id:
                return_todo = todo
        response_object['todo'] = return_todo
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_todo(todo_id)
        TODO.append({
            'id': uuid.uuid4().hex,
            'todo': post_data.get('todo'),
            'assignee': post_data.get('assignee'),
            'read': post_data.get('read'),
        })
        response_object['message'] = 'todo updated!'
    if request.method == 'DELETE':
        remove_todo(todo_id)
        response_object['message'] = 'todo removed!'
    return jsonify(response_object)

def remove_todo(todo_id):
    for todo in TODO:
        if todo['id'] == todo_id:
            TODO.remove(todo)
            return True
    return False


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
