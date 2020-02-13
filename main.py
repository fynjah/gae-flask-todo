import datetime

from flask import Flask, render_template, jsonify

from google.cloud import ndb

app = Flask(__name__)

client = ndb.Client()


def serialize_todos(todos=[]):
    return [dict(t.to_dict(), **dict(id=t.key.id())) for t in todos]


class Todo(ndb.Model):
    title = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    checked = ndb.BooleanProperty(default=False)


@app.route('/')
def root():
    todo = Todo(title="Lorem ipsum dolor sit amet, consectetur adipiscing.")

    with client.context():
        #todo.put()
        todos = Todo.query().order('-timestamp').fetch()

    return render_template('index.html', times=todos)


@app.route('/json')
def json():
    with client.context():
        todos = Todo.query().order('-timestamp').fetch()
    return jsonify(serialize_todos(todos))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)