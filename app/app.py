from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import datetime
from bron_service import BronService
from bron_model import BronSchema
from item_service import ItemService
from item_model import ItemSchema

import json

app = Flask(__name__)
# Cors moet weg in productie
CORS(app) 

@app.route("/")
def welkom():
    return "Welkom!"

@app.route("/bronnen", methods=["GET"])
def geef_bronnen():
    return jsonify(BronService().selectAll())

@app.route("/bron", methods=["POST"])
def create_bron():
    return jsonify(BronService().create(request.get_json()))

@app.route("/items", methods=["GET"])
def geef_items():
    return jsonify(ItemService().selectAll())

@app.route("/items/<datum>", methods=["GET"])
def geef_items_op_datum(datum):
    a_datetime = datetime.datetime.strptime(datum,"%d-%m-%Y") 
    return jsonify(ItemService().selectByDay(int(a_datetime.timestamp())))

@app.route("/items/bron/<bron>", methods=["GET"])
def geef_items_per_bron(bron):
    return jsonify(ItemService().selectBySource(bron))

@app.route("/items/statistics", methods=["GET"])
def geef_item_statistics():
    return jsonify(ItemService().selectStatistics())

@app.route("/items/uitgelicht", methods=["GET"])
def geef_items_uitgelicht():
    return jsonify(ItemService().selectByUitgelicht())    

@app.route("/item", methods=["POST"])
def create_item():
    return jsonify(ItemService().create(request.get_json()))

@app.route("/items/zoeken", methods=["POST"])
def zoek_items():
    return jsonify(ItemService().selectBySearch(request.get_json()))    


if __name__ == "__main__":
    BronSchema()
    ItemSchema()
    app.run()