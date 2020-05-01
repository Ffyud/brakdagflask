class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('brakdag.db')
        self.create_bron_table()

    def create_bron_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "bron" (
          id INTEGER PRIMARY KEY,
          name TEXT,
          link TEXT,
          logo TEXT
        );
        """

        self.conn.execute(query)

class bronModel:
    TABLENAME = "BRON"

    def __init__(self):
        self.conn = sqlite3.connect('brakdag.db')

    def create(self, name, link):
        query = f'insert into {TABLENAME} ' \
                f'(name, link) ' \
                f'values ("{name}","{link}")'
        
        result = self.conn.execute(query)
        return result

    def selectAll():
        query = f'select * ' \
                f'from {TABLENAME}' 

        result = self.conn.execute(query)
        return result 

    def selectByName(name):
        query = f'select * ' \
                f'from {TABLENAME} ' \
                f'where name = "{name}"' 

        result = self.conn.execute(query)
        return result        