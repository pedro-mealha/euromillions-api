import os
import psycopg2
import psycopg2.extras
from urllib.parse import urlparse

class Database():
    def __init__(self):
        try:
            if hasattr(self, 'conn') and self.conn != None:
                self.close()

            result = urlparse(os.getenv("DATABASE_URL"))
            username = result.username
            password = result.password
            database = result.path[1:]
            hostname = result.hostname
            port = result.port
            schema = os.getenv("DB_SCHEMA")

            self.conn = psycopg2.connect(
                database=database,
                user=username,
                password=password,
                host=hostname,
                port=port,
                options="-c search_path="+schema
            )
            self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        except psycopg2.Error as error:
            print ("Oops! An exception has occured:", error)

    def getCursor(self):
        return self.cur

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
