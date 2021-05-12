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
        self.cursor = self.mysql.connection.cursor()
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
        self.connection.commit()
        self.cursor.close()

class BronModel:
    TABLENAME = "Bron"

    def __init__(self):
        self.cursor = self.mysql.connection.cursor()

    def create(self, params):
        print (params)
        query = f'insert into {self.TABLENAME} ' \
                f'(title, link_rss, logo, description, link_home) ' \
                f'values ("{params.get("title")}", ' \
                f'"{params.get("link_rss")}", ' \
                f'"{params.get("logo")}", ' \
                f'"{params.get("description")}", ' \
                f'"{params.get("link_home")}")'
        
        result = self.cursor.execute(query)
        self.connection.commit()

    def selectAll(self):
        query = f'select * ' \
                f'from {self.TABLENAME}' 
        self.connection.row_factory = dict_factory
        result_set = self.cursor.execute(query).fetchall()
        return result_set