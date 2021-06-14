from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/api/")
def response():
    data = {
        "key": "value"
    }
    return jsonify(data)


@app.route("/api/health")
def healthcheck():
    return "ok", 200
