import re
import typing

from .database import Database
from .constants import Flair


class User:
    @staticmethod
    def find_users_by_notification_count_greater_than(db: Database, count: int) -> list:
        results = db.query("SELECT username FROM user WHERE notification_count > ?", [count])
        return [User(username=result[0]) for result in results]

    def __init__(self, **kwargs):
        self.id: int = kwargs.get("id", None)
        self.date_created: str = kwargs.get("date_created", None)
        self.date_updated: str = kwargs.get("date_updated", None)
        self.username: str = kwargs.get("username", None)
        self.notification_count: int = kwargs.get("notification_count", None)
        self.game: typing.Set[str] = kwargs.get("game", set())
        self.day: typing.Set[str] = kwargs.get("day", set())
        self.timezone: typing.Set[str] = kwargs.get("timezone", set())
        self.nsfw: bool = kwargs.get("nsfw", False)
        self.keyword: str = kwargs.get("keyword", None)
        self.flair: int = kwargs.get("flair", Flair.DEFAULT.value)
        self.online: int = kwargs.get("online", 1)

    def find_users(self, db: Database) -> list:
        query = "SELECT username, keyword FROM user WHERE  "

        query += "(" + "or".join([" game like ? " for _ in self.game]) + ") "
        params = [f"%{game}%" for game in self.game]

        if self.nsfw == 1:
            query += "and nsfw = 1 "

        if self.timezone:
            query += "and (timezone is null or " + "or".join([" timezone REGEXP ? " for _ in self.timezone]) + ") "
            params.extend([fr"\b{re.escape(tz)}\b" for tz in self.timezone])
        else:
            query += "and timezone is null "

        if self.day:
            query += "and (day is null or " + "or".join([" day like ? " for _ in self.day]) + ") "
            params.extend([f"%{day}%" for day in self.day])
        else:
            query += "and day is null "

        query += "and (flair & ?) > 0 "
        params.append(self.flair)

        if self.online == 1:
            query += "and online != -1"
        else:
            query += "and online != 1"

        query += "order by notification_count asc"
        data = db.query(query, params)
        if data:
            return [User(username=i[0], keyword=i[1]) for i in data]
        return []

    def exists(self, db: Database) -> bool:
        return bool(db.query("SELECT EXISTS (SELECT id FROM user WHERE username = ?)", [self.username])[0][0])

    def save(self, db: Database) -> None:
        params = []
        params.append(','.join(self.game))
        params.append(','.join(self.timezone) if self.timezone else None)
        params.append(','.join(self.day) if self.day else None)
        params.append(int(self.nsfw))
        params.append(self.keyword)
        params.append(self.flair)
        params.append(self.username)
        if self.exists(db):
            db.save("UPDATE user SET date_updated = CURRENT_TIMESTAMP, game = ?, timezone = ?, day = ?, nsfw = ?, keyword = ?, flair = ? WHERE username = ?", params)
        else:
            db.save("INSERT INTO user (game, timezone, day, nsfw, keyword, flair, username) VALUES (?, ?, ?, ?, ?, ?, ?)", params)

    def delete(self, db: Database) -> None:
        if self.username is not None:
            db.save("DELETE FROM user WHERE username = ?", [self.username])

    def update_notification_count(self, db: Database) -> None:
        db.save("UPDATE user SET notification_count = notification_count + 1 WHERE username = ?", [self.username])
