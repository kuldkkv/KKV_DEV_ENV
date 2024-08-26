from flask import Flask, jsonify, request

import datetime

app = Flask(__name__)


@app.route('/', methods = ['GET'])
def home():
    now = str(datetime.datetime.now())
    data = 'hello world at ' + now
    return jsonify({'data': data})

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8005)
