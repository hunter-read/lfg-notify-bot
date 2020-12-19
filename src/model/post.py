import typing

from .database import Database


class Post:
    @staticmethod
    def __parse_results(results: list) -> list:
        posts = []
        for result in results:
            post = Post(id=result[0])
            post.date_created = result[1]
            post.date_updated = result[2]
            post.submission_id = result[3]
            post.flair = result[4]
            post.game = set(result[5].split(',')) if result[5] else None
            post.day = set(result[6].split(',')) if result[6] else None
            post.timezone = set(result[7].split(',')) if result[7] else None
            post.flag = result[8].split(',') if result[8] else None
            post.time = result[9]
            post.online = bool(result[10])
            post.nsfw = bool(result[11])
            post.permalink = result[12]
            posts.append(post)
        return posts

    @classmethod
    def find_post_by_date_created_greater_than_and_no_flair(cls, db, date: str) -> list:
        results = db.query("SELECT * FROM post WHERE date_created > ? and flair is null", [date])
        return cls.__parse_results(results)

    @classmethod
    def find_post_by_submission_id(cls, db, submission_id: str) -> list:
        results = db.query("SELECT * FROM post WHERE submission_id = ?", [submission_id])
        return cls.__parse_results(results)

    def __init__(self, **kwargs):
        self.id: int = kwargs.get("id", None)
        self.date_created: str = kwargs.get("date_created", None)
        self.date_updated: str = kwargs.get("date_updated", None)
        self.submission_id: str = kwargs.get("submission_id", None)
        self.flair: str = kwargs.get("flair", None)
        self.game: typing.Set[str] = kwargs.get("game", set())
        self.day: typing.Set[str] = kwargs.get("day", set())
        self.timezone: typing.Set[str] = kwargs.get("timezone", set())
        self.flag: typing.List[str] = kwargs.get("flag", [])
        self.time: str = kwargs.get("time", None)
        self.online: bool = kwargs.get("online", False)
        self.nsfw: bool = kwargs.get("nsfw", False)
        self.permalink: str = kwargs.get("permalink", None)

    def exists(self, db: Database) -> bool:
        return bool(db.query("SELECT EXISTS (SELECT id FROM post WHERE submission_id = ?)", [self.submission_id])[0][0])

    def update_flair(self, db) -> None:
        db.save("UPDATE post SET flair = ? WHERE id = ?", [self.flair, self.id])

    def save(self, db: Database) -> None:
        params = []
        params.append(self.submission_id)
        params.append(self.flair)
        params.append(','.join(self.game) if self.game else None)
        params.append(','.join(self.day) if self.day else None)
        params.append(','.join(self.timezone) if self.timezone else None)
        params.append(','.join(self.flag) if self.flag else None)
        params.append(self.time)
        params.append(int(self.online))
        params.append(int(self.nsfw))
        params.append(self.permalink)
        db.save("INSERT INTO post (submission_id, flair, game, day, timezone, flag, time, online, nsfw, permalink) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
