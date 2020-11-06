class UserRequest:
    def __init__(self, **kwargs):
        self.username = kwargs.get("username", None)
        self.date_created = kwargs.get("date_created", None)
        self.game = kwargs.get("game", set())
        self.days = kwargs.get("days", set())  # day_of_week
        self.timezone = kwargs.get("timezone", set())
        self.nsfw = kwargs.get("nsfw", 0)

    def find_users(self, db):
        query = "SELECT username FROM user_request WHERE  "

        query += "(" + "or".join([" game like ? " for _ in self.game]) + ") "
        params = [f"%{game}%" for game in self.game]

        if self.nsfw == 0:
            query += "and nsfw = 0 "

        if self.timezone:
            query += "and (timezone is null or " + "or".join([" timezone like ? " for _ in self.timezone]) + ") "
            params.extend([f"%{timezone}%" for timezone in self.timezone])

        if self.days:
            query += "and (day_of_week is null or " + "or".join([" day_of_week like ? " for _ in self.days]) + ") "
            params.extend([f"%{day}%" for day in self.days])

        return db.query(query, params)

    def save(self, db):
        self.delete(db)
        params = []
        params.append(self.username)
        params.append(','.join(self.game))
        params.append(','.join(self.timezone) if self.timezone else None)
        params.append(','.join(self.days) if self.days else None)
        params.append(self.nsfw)
        db.save("INSERT INTO user_request (id, date_created, username, game, timezone, day_of_week, nsfw) VALUES (null, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)", params)
        return

    def delete(self, db):
        if self.username is not None:
            db.save("DELETE FROM user_request WHERE username = ?", [self.username])
