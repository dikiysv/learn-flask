import math

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/sqrt', methods=['GET'])
def add_message():
    print(request.args)
    if 'value' not in request.args:
        return 'No value in request', 400
    response = {'result': math.sqrt(float(request.args['value']))}
    return jsonify(response)


if __name__ == '__main__':
    app.run()
