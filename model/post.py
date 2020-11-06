class Post:
    def __init__(self, **kwargs):
        self.post_date = kwargs.get("post_date", None)
        self.game = kwargs.get("game", set())
        self.days = kwargs.get("days", set())
        self.timezone = kwargs.get("timezone", set())
        self.time = kwargs.get("time", None)
        self.nsfw = kwargs.get("nsfw", 0)
        self.flair = kwargs.get("flair", None)
        self.permalink = kwargs.get("permalink", None)
        self.online = kwargs.get("online", 1)

    def save(self, db):
        db.save("INSERT INTO post (id, post_date, game, flair, timezone, days, times, nsfw, permalink, online) VALUES (null, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?)", [','.join(self.game), self.flair, ','.join(self.timezone), ','.join(self.days), self.time, self.nsfw, self.permalink, self.online])
