import sqlite3


class Database(object):
    def __init__(self, db):
        self.__DB_LOCATION = db
        self.__db_connection = sqlite3.connect(self.__DB_LOCATION)
        self.__db_cursor = None

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.close()

    def close(self):
        self.__db_connection.close()

    def query(self, query, params):
        self.__db_cursor = self.__db_connection.cursor()
        data = list(self.__db_cursor.execute(query, params))
        self.__db_cursor.close()
        return data

    def save(self, query, params):
        self.__db_cursor = self.__db_connection.cursor()
        self.__db_cursor.execute(query, params)
        self.__db_connection.commit()
        self.__db_cursor.close()
