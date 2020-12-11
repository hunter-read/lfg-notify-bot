import typing
from .database import Database


class Post:
    def __init__(self, **kwargs):
        self.submission_id: str = kwargs.get("submission_id", None)
        self.post_date: str = kwargs.get("post_date", None)
        self.game: typing.Set[str] = kwargs.get("game", set())
        self.days: typing.Set[str] = kwargs.get("days", set())
        self.timezone: typing.Set[str] = kwargs.get("timezone", set())
        self.time: str = kwargs.get("time", None)
        self.nsfw: int = kwargs.get("nsfw", 0)
        self.flair: str = kwargs.get("flair", None)
        self.permalink: str = kwargs.get("permalink", None)
        self.online: int = kwargs.get("online", 1)

    def save(self, db: Database) -> None:
        params = []
        params.append(','.join(self.game) if self.game else None)
        params.append(self.flair)
        params.append(','.join(self.timezone) if self.timezone else None)
        params.append(','.join(self.days) if self.days else None)
        params.append(self.time)
        params.append(self.nsfw)
        params.append(self.permalink)
        params.append(self.online)
        params.append(self.submission_id)
        db.save("INSERT INTO post (id, post_date, game, flair, timezone, days, times, nsfw, permalink, online, submission_id) VALUES (null, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
