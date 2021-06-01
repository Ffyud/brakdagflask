from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL
import time
from datetime import date
from datetime import datetime
from urllib.parse import urlparse
import os
import time
import logging
from bron_service import BronService
from bron_model import BronSchema
from item_service import ItemService
from item_model import ItemSchema
import json

DATA_PATH = "./database"

if os.path.exists(DATA_PATH) == False:
    os.mkdir(DATA_PATH)

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'brakdag'
app.config['MYSQL_PASSWORD'] = 'brakdag'
app.config['MYSQL_DB'] = 'brakdag'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Cors moet weg in productie
# CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "http://95.217.165.225:1337"}})


@app.route("/")
def welkom():
    return "Welkom!"


@app.route("/bron", methods=["POST"])
def post_bron():
    request_data = request.get_json()
    title = request_data['title']
    link_rss = request_data['link_rss']
    logo = request_data['logo']
    description = request_data['description']
    link_home = request_data['link_home']

    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO Bron (title, link_rss, logo, description, link_home)
                       VALUES (%s, %s, %s, %s, %s)''', (title, link_rss, logo, description, link_home))
    mysql.connection.commit()
    cursor.close()
    return f'jeej!'


@app.route("/bron", methods=["GET"])
def get_bron():
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT *
                       FROM Bron ''')
    mysql.connection.commit()
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)


@app.route("/items", methods=["GET"])
def get_items():
    # Timestamp van middernacht tot aan huidige tijd
    vandaag = date.today()
    middernacht = datetime.combine(vandaag, datetime.min.time())
    timestampMiddernacht = int(middernacht.timestamp())
    timestampNu = int(time.time())

    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT a.*, b.title as bron_title, b.logo, b.link_home
                       FROM Item as a
                       JOIN Bron as b ON a.bron_id = b.id
                       WHERE timestamp_publicatie >= %s
                       AND timestamp_publicatie <= %s
                       ORDER BY timestamp_gevonden DESC''', (timestampMiddernacht, timestampNu))
    mysql.connection.commit()
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)


@app.route("/items/uitgelicht", methods=["GET"])
def get_items_uitgelicht():
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT a.*, b.title as bron_title, b.logo, b.link_home
                       FROM Item as a
                       JOIN Bron as b ON a.bron_id = b.id
                       WHERE a.uitgelicht = 1
                       ORDER BY timestamp_gevonden DESC''')
    mysql.connection.commit()
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)


@app.route("/items/statistics", methods=["GET"])
def get_item_statistics():
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT COUNT(*) as aantal_items, b.*
                       FROM Item as a
                       JOIN Bron as b ON a.bron_id = b.id
                       GROUP BY b.id''')
    mysql.connection.commit()
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)


@app.route("/item", methods=["POST"])
# @cross_origin(resources={r"/*": {"origins": ["http://localhost:3000", "-"]}})
def post_item():
    request_data = request.get_json()
    title = request_data['title']
    link = request_data['link']
    description = request_data['description']
    timestamp_publicatie = request_data['timestamp_publicatie']
    timestampVanNu = int(time.time())

    if title and link:
        # Controleren of het artikel nog niet bestaat
        cursor = mysql.connection.cursor()
        cursor.execute(''' SELECT id FROM Item 
                           WHERE title = %s AND link = %s''', (title, link))
        mysql.connection.commit()
        aantalArtikelenGevonden = len(cursor.fetchall())
        cursor.close()

        if aantalArtikelenGevonden == 0:

            # De link naar het artikel even uit elkaar trekken
            linkParse = urlparse(link)
            linkScheme = linkParse.scheme + "://"
            linkNetLoc = linkParse.netloc
            linkHomeUrl = linkScheme + linkNetLoc

            # Een bron zoeken bij het artikel op basis van de link
            cursor = mysql.connection.cursor()
            cursor.execute(''' SELECT id, title 
                               FROM Bron 
                               WHERE link_home = %s''', (linkHomeUrl))
            mysql.connection.commit()
            aantalArtikelenGevonden = len(cursor.fetchall())
            resultBronRij = cursor.fetchone()
            cursor.close()

            # Als er geen bron gevonden wordt, kiezen we bronId 0
            if resultBronRij == None:
                resultBronId = 0
            else:
                resultBronId = resultBronRij[0]

            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO Item 
                               (title, link, timestamp_publicatie, timestamp_gevonden, description, bron_id) 
                               VALUES (%s, %s, %s, %s, %s, %s)''', (title, link, timestamp_publicatie, timestampVanNu, description, resultBronId))
            mysql.connection.commit()
            cursor.close()

            return {
                "resultaat": "goed",
                "titel": title,
                "link": link,
                "bronIdGevonden": resultBronId
            }
        else:
            return {
                "resultaat": "artikel_bestaat_al",
                "titel": title,
                "link": link
            }
    else:
        return "mislukt"


@app.route("/items/<datum>", methods=["GET"])
def geef_items_op_datum(datum):
    a_datetime = datetime.datetime.strptime(datum, "%d-%m-%Y") 
    return jsonify(ItemService().selectByDay(int(a_datetime.timestamp())))


@app.route("/items/bron/<bron>", methods=["GET"])
def geef_items_per_bron(bron):
    return jsonify(ItemService().selectBySource(bron))


@app.route("/items/zoeken", methods=["POST"])
def zoek_items():
    return jsonify(ItemService().selectBySearch(request.get_json()))

# @app.route("/item", methods=["POST"])
# @cross_origin(resources={r"/*": {"origins": ["http://localhost:3000", "-"]}})
# def create_item():
#     return jsonify(ItemService().create(request.get_json()))

# @app.route("/items/statistics", methods=["GET"])
# def geef_item_statistics():
#     return jsonify(ItemService().selectStatistics())


# @app.route("/items/uitgelicht", methods=["GET"])
# def geef_items_uitgelicht():
#     return jsonify(ItemService().selectByUitgelicht())

# @app.route("/bronnen", methods=["GET"])
# def geef_bronnen():
#     return jsonify(BronService().selectAll())

# @app.route("/bron", methods=["POST"])
# def create_bron():
#     return jsonify(BronService().create(request.get_json()))

# @app.route("/items", methods=["GET"])
# def geef_items():
#     return jsonify(ItemService().selectAll())

if __name__ == "__main__":
    BronSchema()
    ItemSchema()
    app.run()
