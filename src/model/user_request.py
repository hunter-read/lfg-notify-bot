import typing
from .database import Database


class UserRequest:
    def __init__(self, **kwargs):
        self.username: str = kwargs.get("username", None)
        self.date_created: str = kwargs.get("date_created", None)
        self.game: typing.Set[str] = kwargs.get("game", set())
        self.days: typing.Set[str] = kwargs.get("days", set())  # day_of_week
        self.timezone: typing.Set[str] = kwargs.get("timezone", set())
        self.nsfw: int = kwargs.get("nsfw", 0)

    def find_users(self, db: Database) -> tuple:
        query = "SELECT username FROM user_request WHERE  "

        query += "(" + "or".join([" game like ? " for _ in self.game]) + ") "
        params = [f"%{game}%" for game in self.game]

        if self.nsfw == 1:
            query += "and nsfw = 1 "

        if self.timezone:
            query += "and (timezone is null or " + "or".join([" timezone REGEXP ? " for _ in self.timezone]) + ") "
            params.extend([f"\\b{timezone}\\b".replace('+', '\\+') for timezone in self.timezone])
        else:
            query += "and timezone is null "

        if self.days:
            query += "and (day_of_week is null or " + "or".join([" day_of_week like ? " for _ in self.days]) + ") "
            params.extend([f"%{day}%" for day in self.days])
        else:
            query += "and day_of_week is null "

        query += "order by notification_count asc"
        data = db.query(query, params)
        if data:
            return [i[0] for i in data]
        return []

    def save(self, db: Database) -> None:
        params = []
        params.append(','.join(self.game))
        params.append(','.join(self.timezone) if self.timezone else None)
        params.append(','.join(self.days) if self.days else None)
        params.append(self.nsfw)
        if db.query("SELECT EXISTS (SELECT id FROM user_request WHERE username = ?)", [self.username])[0][0]:
            params.append(self.username)
            db.save("UPDATE user_request SET game = ?, timezone = ?, day_of_week = ?, nsfw = ? WHERE username = ?", params)
        else:
            params.insert(0, self.username)
            db.save("INSERT INTO user_request (id, date_created, username, game, timezone, day_of_week, nsfw) VALUES (null, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)", params)

    def delete(self, db: Database) -> None:
        if self.username is not None:
            db.save("DELETE FROM user_request WHERE username = ?", [self.username])

    def update_notification_count(self, db: Database) -> None:
        db.save("UPDATE user_request SET notification_count = notification_count + 1 WHERE username = ?", [self.username])
