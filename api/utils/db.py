import os
import psycopg2
import psycopg2.extras

class Database():
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                database=os.getenv("DB_SCHEMA"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
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
