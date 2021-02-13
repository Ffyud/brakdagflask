import sqlite3
import json
import os
import logging

DATA_PATH = "./database"
TABLENAME = "Bron"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
    
class BronSchema:

    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(DATA_PATH,"brakdag-database.db"))
        self.cursor = self.conn.cursor()
        self.create_item_table()

    def create_bron_table(self):
        query = f'CREATE TABLE IF NOT EXISTS "{self.TABLENAME}" (' \
                f'id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                f'title TEXT, ' \
                f'link_rss TEXT, ' \
                f'logo TEXT, ' \
                f'description TEXT, ' \
                f'link_home TEXT);'
        print("execute die query dan")
        self.cursor.execute(query)
        self.conn.commit()
        self.conn.close()

class BronModel:
    TABLENAME = "Bron"

    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(DATA_PATH,"brakdag-database.db"))

    def create(self, params):
        print (params)
        query = f'insert into {self.TABLENAME} ' \
                f'(title, link_rss, logo, description, link_home) ' \
                f'values ("{params.get("title")}", ' \
                f'"{params.get("link_rss")}", ' \
                f'"{params.get("logo")}", ' \
                f'"{params.get("description")}", ' \
                f'"{params.get("link_home")}")'
        
        result = self.conn.execute(query)
        self.conn.commit()

    def selectAll(self):
        query = f'select * ' \
                f'from {self.TABLENAME}' 
        self.conn.row_factory = dict_factory
        result_set = self.conn.execute(query).fetchall()
        return result_set