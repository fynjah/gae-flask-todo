import datetime

from flask import Flask, render_template

from google.cloud import datastore

app = Flask(__name__)

datastore_client = datastore.Client()


@app.route('/')
def root():
    dummy_times = []

    return render_template('index.html', times=dummy_times)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)