from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def response():
    data = {
        "key": "value"
    }
    return jsonify(data)
