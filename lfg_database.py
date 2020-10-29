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


class Post:
    def __init__(self, post_date=None, game=None, days=None, timezone=None, time=None, nsfw=0, flair=None, permalink=None):
        self.post_date = post_date
        self.game = game
        self.days = days
        self.timezone = timezone
        self.time = time
        self.nsfw = nsfw
        self.flair = flair
        self.permalink = permalink
    
    def save(self, db):
        db.save("INSERT INTO post (id, post_date, game, flair, timezone, days, times, nsfw, permalink) VALUES (null, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?)", [self.game, self.flair, self.timezone, ','.join(day.upper() for day in self.days), self.time, self.nsfw, self.permalink])
        
class UserRequest:
    def __init__(self, date_created=None, username=None, game=None, days=None, timezone=None, nsfw=0):
        self.date_created = date_created
        self.username = username
        self.game = game
        self.days = days #day_of_week 
        self.timezone = timezone
        self.nsfw = nsfw

    def find_users(self, db):
        query = "SELECT username FROM user_request WHERE game like ? "
        params = [f"%{self.game}%"]

        if self.nsfw == 0:
            query += "and nsfw = 0 "

        if self.timezone is not None:
            if "," in self.timezone:
                a,b = self.timezone.split(",")
                query += "and (timezone like ? or timezone like ? or timezone = '')"
                params.append(f"%{a}%")
                params.append(f"%{b}%")
            else:
                query += "and (timezone like ? or timezone = '')"
                params.append(f"%{self.timezone}%")
        
        if self.days is not None:
            num_days = len(self.days)
            query += "(day of week = '' or "
            for i in range(num_days):
                day = self.days.pop()
                query += "day_of_week like ? "
                params.append(f"%{day.upper()}%")
                if i < (num_days - 1):
                    query += "or "
            query += ") "


        return db.query(query, params)
    
    def save(self, db):
        self.delete(db)
        db.save("INSERT INTO user_request (id, date_created, username, game, timezone, day_of_week, nsfw) VALUES (null, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)", [self.username, self.game, self.timezone, self.days, self.nsfw])
        return
    
    def delete(self, db):
        if self.username is not None:
            db.save("DELETE FROM user_request WHERE username = ?", [self.username])
