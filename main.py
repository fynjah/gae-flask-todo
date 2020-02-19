import os
from functools import wraps
from flask import Flask, render_template, jsonify, session, request, abort, make_response
from google.cloud import ndb
from google.oauth2 import id_token
from google.auth.transport import requests
from models import Todo


app = Flask(__name__)
# Gets sensible data from .env
app.secret_key = os.environ.get('TODO_SECRET_KEY', None)
CLIENT_ID = os.environ.get('TODO_CLIENT_ID')


client = ndb.Client()


def serialize_todo(todo):
    '''
    Simple function to add object id to dict from model.
    '''
    return dict(todo.to_dict(), **dict(id=todo.key.id()))


def serialize_todos(todos=[]):
    '''
    Do same as abobe, but in list generator.
    '''
    return [serialize_todo(t) for t in todos]


def login_required(f):
    '''
    Decorator to check userid in session. 
    userid can be present in session only if user is authorized.
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'userid' in session:
            abort(make_response(jsonify({"error": "You are not authorized."}), 401))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def root():
    '''
    Simply returns rendered html with sign-in button.
    '''
    return render_template('auth.html', CLIENT_ID=CLIENT_ID)


@app.route('/auth')
def auth():
    '''
    Authorization view. Reveives token and checks it at google.
    If ok - google returs userinfo and wee add userid in session.
    '''
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
        # Returns body of app.
        return render_template('index.html')
    except ValueError:
        return jsonify({"error": "Token is not valid."}), 400


@app.route('/api/v1/todos', methods=['POST', 'GET'])
@login_required
def api_todos():
    '''
    An endpoint to create and receive todos.
    '''
    status_code = 200
    with client.context():
        if request.method == 'POST':
            title = request.values.get('title', None)
            if not title:
                return jsonify({'error': "Field \'title\' is empty."})
            todo = Todo(title=request.values.get('title'),
                        userid=session['userid'])
            todo.put()
            status_code = 201
            # Yeah, we could return here newly created object,
            # but I decided to return the whole list.
            # return jsonify(serialize_todo(todo))
        todos = Todo.query().filter(Todo.userid == session['userid'])
        todos = todos.fetch()
    return jsonify(serialize_todos(todos)), status_code


@app.route('/api/v1/todos/<int:todo_id>', methods=['PUT', 'DELETE'])
@login_required
def api_todo_detail(todo_id):
    '''
    An endpoint to update todo and also to delete.
    Checks permission for update.
    '''
    userid = session['userid']
    with client.context():
        todo = Todo.get_by_id(todo_id)
        if not todo.userid == userid:
            return {"error": "Todo does not exist."}, 400
        if request.method == 'PUT':
            todo.checked = bool(request.values.get('checked', False))
            todo.put()
            return jsonify(serialize_todo(todo))
        if request.method == 'DELETE':
            todo.key.delete()
            return '', 204


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

