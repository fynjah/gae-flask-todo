import os
from flask import Flask, render_template, jsonify, session, request
from google.cloud import ndb
from google.oauth2 import id_token
from google.auth.transport import requests
from models import Todo


app = Flask(__name__)
app.secret_key = os.environ.get('TODO_SECRET_KEY', None)
CLIENT_ID = os.environ.get('TODO_CLIENT_ID')


client = ndb.Client()


def serialize_todo(todo):
    # I know, som
    return dict(todo.to_dict(), **dict(id=todo.key.id()))


def serialize_todos(todos=[]):
    return [serialize_todo(t) for t in todos]


@app.route('/')
def root():
    return render_template('auth.html', CLIENT_ID=CLIENT_ID)


@app.route('/auth')
def auth():
    token = request.args.get('token')
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # ID token is valid.
        # Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
        session['userid'] = userid
        return render_template('index.html')
    except ValueError:
        return 'Error'


@app.route('/api/v1/todos', methods=['POST', 'GET'])
def api_todos():
    if not 'userid' in session:
        return 'Error not userid'
    with client.context():
        if request.method == 'POST':
            title = request.values.get('title', None)
            if not title:
                return 'Error title'
            todo = Todo(title=request.values.get('title'),
                        userid=session['userid'])
            todo.put()
        todos = Todo.query().filter(Todo.userid == session['userid'])
        todos = todos.fetch()
    return jsonify(serialize_todos(todos))


@app.route('/api/v1/todos/<int:todo_id>', methods=['PUT', 'DELETE'])
def api_todo_detail(todo_id):
    if not 'userid' in session:
        return 'Error not userid'
    userid = session['userid']
    with client.context():
        todo = Todo.get_by_id(todo_id)
        if not todo.userid == userid:
            return '404'
        if request.method == 'PUT':
            todo.checked = bool(request.values.get('checked', False))
            todo.put()
            return jsonify(serialize_todo(todo))
        if request.method == 'DELETE':
            todo.key.delete()
            return '204'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

