import sqlite3
import json

class Schema:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('brakdag-database.db')
            return self.conn
        except Error as e:
            print(e)
        
        self.create_bron_table()

    def __del__(self):
        self.conn.commit()
        self.conn.close()    

    def create_bron_table(self):
        query = f'CREATE TABLE IF NOT EXISTS "Bron" (' \
                f'id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                f'title TEXT, ' \
                f'link TEXT, ' \
                f'logo TEXT);'
        
        self.conn.execute(query)
        self.conn.commit()
        self.conn.close()

class bronModel:
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