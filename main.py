import os
from flask import Flask, render_template, jsonify, session, request
from google.cloud import ndb
from google.oauth2 import id_token
from google.auth.transport import requests
from models import Todo


app = Flask(__name__)
app.secret_key = os.environ.get('TODO_SECRET_KEY', None)
CLIENT_ID = os.environ.get('TODO_CLIENT_ID')
print(CLIENT_ID)
print(app.secret_key)


client = ndb.Client()


def serialize_todos(todos=[]):
    return [dict(t.to_dict(), **dict(id=t.key.id())) for t in todos]


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

@app.route('/json')
def json():
    with client.context():
        todos = Todo.query().order('-timestamp').fetch()
    return jsonify(serialize_todos(todos))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
