import os
from psycopg import conninfo, connect, Error, Connection, rows

class Database():
    def __init__(self):
        try:
            if hasattr(self, 'conn') and self.conn != None:
                self.close()

            db_url = os.getenv("DATABASE_URL")
            schema = os.getenv("DB_SCHEMA")

            db_info = conninfo.conninfo_to_dict(db_url, options="-c search_path="+schema)

            self.conn = connect(**db_info, row_factory=rows.dict_row)
            self.cur = self.conn.cursor()
        except Error as error:
            print ("Error while connecting to db:", error)

    def getCursor(self):
        return self.cur

    def getConn(self) -> Connection:
        return self.conn

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
