import sqlite3
import json

class Schema:
    TABLENAME = "Bron"

    def __init__(self):
        self.conn = sqlite3.connect('brakdag-database.db')
        self.create_bron_table()

    def create_bron_table(self):
        query = f'CREATE TABLE IF NOT EXISTS "{self.TABLENAME}" (' \
                f'id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                f'title TEXT, ' \
                f'link TEXT, ' \
                f'logo TEXT);'        
        
        result = self.conn.execute(query)
        self.conn.commit()

class BronModel:
    TABLENAME = "Bron"

    def __init__(self):
        self.conn = sqlite3.connect('brakdag-database.db')

    def create(self, params):
        print (params)
        query = f'insert into {self.TABLENAME} ' \
                f'(title, link) ' \
                f'values ("{params.get("title")}","{params.get("link")}")'
        
        result = self.conn.execute(query)
        self.conn.commit()

    def selectAll(self):
        query = f'select * ' \
                f'from {self.TABLENAME}' 

        result_set = self.conn.execute(query).fetchall()
        return result_set