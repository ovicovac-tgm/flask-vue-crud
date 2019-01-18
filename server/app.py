import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)

TODOS = [
    {
        'id': uuid.uuid4().hex,
        'todo': 'something',
        'assignee': 'Oliver',
        'done': True
    },
    {
        'id': uuid.uuid4().hex,
        'todo': 'cool stuff',
        'assignee': 'cool dude',
        'done': False,
    },
    {
        'id': uuid.uuid4().hex,
        'todo': 'dancing',
        'assignee': 'dancer',
        'done': True,
    }
]

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/todos', methods=['GET', 'POST'])
def all_todos():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        TODOS.append({
            'id': uuid.uuid4().hex,
            'todo': post_data.get('todo'),
            'assignee': post_data.get('assignee'),
            'done': post_data.get('done'),
        })
        response_object['message'] = 'todo added!'
    else:
        response_object['todos'] = TODOS
    return jsonify(response_object)


@app.route('/todos/<todo_id>', methods=['GET', 'PUT', 'DELETE'])
def single_todo(todo_id):
    response_object = {'status': 'success'}
    if request.method == 'GET':
        # TODO: refactor to a lambda and filter
        return_todo = ''
        for todo in TODOS:
            if todo['id'] == todo_id:
                return_todo = todo
        response_object['todo'] = return_todo
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_todo(todo_id)
        TODOS.append({
            'id': uuid.uuid4().hex,
            'todo': post_data.get('todo'),
            'assignee': post_data.get('assignee'),
            'done': post_data.get('done'),
        })
        response_object['message'] = 'todo updated!'
    if request.method == 'DELETE':
        remove_todo(todo_id)
        response_object['message'] = 'todo removed!'
    return jsonify(response_object)

def remove_todo(todo_id):
    for todo in TODOS:
        if todo['id'] == todo_id:
            TODOS.remove(todo)
            return True
    return False


if __name__ == '__main__':
    app.run(port=8080)
