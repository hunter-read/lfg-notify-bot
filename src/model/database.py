import sqlite3
import typing
import re

def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None

class Database(object):
    def __init__(self, db: str):
        self.__DB_LOCATION: str = db
        self.__db_connection = sqlite3.connect(self.__DB_LOCATION)
        self.__db_connection.create_function("REGEXP", 2, regexp)
        self.__db_cursor = None

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.close()

    def close(self):
        self.__db_connection.close()

    def query(self, query: str, params: typing.List[str]) -> tuple:
        self.__db_cursor = self.__db_connection.cursor()
        data = list(self.__db_cursor.execute(query, params))
        self.__db_cursor.close()
        return data

    def save(self, query: str, params: typing.List[str]) -> None:
        self.__db_cursor = self.__db_connection.cursor()
        self.__db_cursor.execute(query, params)
        self.__db_connection.commit()
        self.__db_cursor.close()
