import sqlite3
import json
import time
import os
from datetime import date
from datetime import datetime
from flask import Response
from urllib.parse import urlparse

DATA_PATH = "./database"
TABLENAME = "Item"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class ItemSchema:

    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(DATA_PATH,"brakdag-database.db"))
        self.cursor = self.conn.cursor()
        self.create_item_table()

    def create_item_table(self):
        query = f'CREATE TABLE IF NOT EXISTS "{self.TABLENAME}" (' \
                f'id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                f'title TEXT, ' \
                f'link TEXT, ' \
                f'timestamp_publicatie INTEGER, ' \
                f'timestamp_gevonden INTEGER, ' \
                f'description TEXT, ' \
                f'uitgelicht INTEGER, ' \
                f'bron_id INTEGER);'
        
        self.cursor.execute(query)
        self.conn.commit()
        self.conn.close()

class ItemModel:
    TABLENAME = "Item" 
    
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(DATA_PATH,"brakdag-database.db"))

    def create(self, params):
        timestampVanNu = int(time.time())
        if params.get("title") and params.get("link"):
            
            # Controleren of het artikel nog niet bestaat
            queryBestaatArtikel = f'select id from {self.TABLENAME} WHERE title = "{params.get("title")}" AND link = "{params.get("link")}"'
            resultBestaatArtikel = self.conn.execute(queryBestaatArtikel)
            aantalArtikelenGevonden = len(resultBestaatArtikel.fetchall())

            if aantalArtikelenGevonden == 0:

                # De link naar het artikel even uit elkaar trekken
                linkParse = urlparse(params.get("link"))
                linkScheme = linkParse.scheme + "://"
                linkNetLoc = linkParse.netloc
                linkHomeUrl = linkScheme + linkNetLoc

                # Een bron zoeken bij het artikel op basis van de link
                getBronBijLink = f'select id, title from Bron where link_home = "{linkHomeUrl}"'
                resultBronBijLink = self.conn.execute(getBronBijLink)
                resultBronRij = resultBronBijLink.fetchone()

                # Als er geen bron gevonden wordt, kiezen we bronId 0
                if resultBronRij == None:
                    resultBronId = 0
                else:    
                    resultBronId = resultBronRij[0]

                query = f'insert into {self.TABLENAME} ' \
                        f'(title, link, timestamp_publicatie, timestamp_gevonden, description, bron_id) ' \
                        f'values ("{params.get("title")}", ' \
                        f'"{params.get("link")}", ' \
                        f'"{params.get("timestamp_publicatie")}", ' \
                        f'{timestampVanNu} , ' \
                        f'"{params.get("description")}", ' \
                        f'{resultBronId})'
                result = self.conn.execute(query)
                self.conn.commit()
                
                return {
                    "resultaat": "goed",
                    "titel": params.get("title"),
                    "link": params.get("link"),
                    "rijenToegevoegd": result.rowcount,
                    "bronIdGevonden": resultBronId
                }
            else:
                return {
                    "resultaat": "artikel_bestaat_al",
                    "titel": params.get("title"),
                    "link": params.get("link")
                }    
        else:
            return Response(status=500, mimetype='application/json')

    def selectAll(self):
        # Timestamp van middernacht tot aan huidige tijd gebruiken
        vandaag = date.today()
        middernacht = datetime.combine(vandaag, datetime.min.time())
        timestampMiddernacht = int(middernacht.timestamp())
        timestampNu = int(time.time())

        query = f'select a.*, b.title as bron_title, b.logo, b.link_home ' \
                f'from {self.TABLENAME} as a ' \
                f'join Bron as b on a.bron_id = b.id ' \
                f'where timestamp_publicatie >= {timestampMiddernacht} ' \
                f'and timestamp_publicatie <= {timestampNu} ' \
                f'order by timestamp_gevonden desc'
        self.conn.row_factory = dict_factory   
        result_set = self.conn.execute(query).fetchall()
        return result_set

    def selectByDay(self, param):
        a_day = param + 86400
        query = f'select a.*, b.title as bron_title, b.logo, b.link_home ' \
                f'from {self.TABLENAME} as a ' \
                f'join Bron as b on a.bron_id = b.id ' \
                f'where timestamp_publicatie >= {param} ' \
                f'and timestamp_publicatie <= {a_day} ' \
                f'order by timestamp_gevonden desc'
        self.conn.row_factory = dict_factory   
        result_set = self.conn.execute(query).fetchall()
        return result_set

    def selectBySource(self, param):
        query = f'select a.*, b.title as bron_title, b.logo, b.link_home ' \
                f'from {self.TABLENAME} as a ' \
                f'join Bron as b on a.bron_id = b.id ' \
                f'where b.id = {param} ' \
                f'order by timestamp_gevonden desc'
        self.conn.row_factory = dict_factory   
        result_set = self.conn.execute(query).fetchall()
        return result_set

    def selectStatistics(self):
        queryGrouped = f'SELECT COUNT(*) as aantal_items, b.* ' \
                       f'FROM Item as a ' \
                       f'JOIN Bron as b ' \
                       f'ON a.bron_id = b.id ' \
                       f'GROUP BY b.id'
        self.conn.row_factory = dict_factory   
        result_set_grouped = self.conn.execute(queryGrouped).fetchall()

        return result_set_grouped

    def selectBySearch(self, param):
        searchString = '%'+str(param.get("term"))+'%'
        query = f'select a.*, b.title as bron_title, b.logo, b.link_home ' \
                f'from {self.TABLENAME} as a ' \
                f'join Bron as b on a.bron_id = b.id ' \
                f'where a.title LIKE ? ' \
                f'order by a.timestamp_gevonden desc'
        self.conn.row_factory = dict_factory   
        result_set = self.conn.execute(query, (searchString,)).fetchall()
        return result_set  

    def selectByUitgelicht(self):
        query = f'select a.*, b.title as bron_title, b.logo, b.link_home ' \
                f'from {self.TABLENAME} as a ' \
                f'join Bron as b on a.bron_id = b.id ' \
                f'where a.uitgelicht = 1 ' \
                f'order by timestamp_gevonden desc'
        self.conn.row_factory = dict_factory   
        result_set = self.conn.execute(query).fetchall()
        return result_set