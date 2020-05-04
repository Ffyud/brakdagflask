from flask import Flask, request, jsonify
from service import BronService
from models import Schema

import json

app = Flask(__name__)

@app.route("/")
def welkom():
    return "Welkom!"

@app.route("/bronnen", methods=["GET"])
def geefBronnen():
    return jsonify(BronService().selectAll())

@app.route("/bron", methods=["POST"])
def create_bron():
    return jsonify(BronService().create(request.get_json()))

if __name__ == "__main__":
    Schema()
    app.run()     