import re
import typing

from .database import Database
from .constants import Flair, Location, Nsfw, PlayByPost, OneShot, Identity, AgeLimit, Vtt


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
        self.nsfw: int = kwargs.get("nsfw", Nsfw.EXCLUDE.value)
        self.keyword: str = kwargs.get("keyword", None)
        self.flair: int = kwargs.get("flair", Flair.DEFAULT.flag)
        self.online: int = kwargs.get("online", Location.ONLINE.value)
        self.play_by_post: int = kwargs.get("play_by_post", PlayByPost.INCLUDE.value)
        self.one_shot: int = kwargs.get("one_shot", OneShot.INCLUDE.value)
        self.lgbtq: int = kwargs.get("lgbtq", Identity.NONE.flag)
        self.age_limit: int = kwargs.get("age_limit", AgeLimit.NONE.value)
        self.vtt: int = kwargs.get("vtt", Vtt.NONE.flag)
        self.match_no_day: bool = kwargs.get("match_no_day", False)
        self.match_no_timezone: bool = kwargs.get("match_no_timezone", False)

    def find_users(self, db: Database) -> list:
        query = "SELECT username, keyword FROM user WHERE  "

        query += "(" + "or".join([" game like ? " for _ in self.game]) + ") "
        params = [f"%{game}%" for game in self.game]

        if bool(self.nsfw):
            query += f"and nsfw != {Nsfw.EXCLUDE.value} "
        else:
            query += f"and nsfw != {Nsfw.ONLY.value} "

        if self.timezone:
            query += "and (timezone is null or " + "or".join([" timezone REGEXP ? " for _ in self.timezone]) + ") "
            params.extend([fr"\b{re.escape(tz)}\b" for tz in self.timezone])
        else:
            query += "and (timezone is null or timezone like '%NOTZ%') "

        if self.day:
            query += "and (day is null or " + "or".join([" day like ? " for _ in self.day]) + ") "
            params.extend([f"%{day}%" for day in self.day])
        else:
            query += "and (day is null or day like '%NODAY%') "

        query += "and (flair & ?) > 0 "
        params.append(self.flair)

        if self.online == Location.ONLINE.value:
            query += f"and online != {Location.OFFLINE.value} "
        elif self.online == Location.OFFLINE.value:
            query += f"and online != {Location.ONLINE.value} "

        if bool(self.play_by_post):
            query += f"and play_by_post != {PlayByPost.EXCLUDE.value} "
        else:
            query += f"and play_by_post != {PlayByPost.ONLY.value} "

        if bool(self.one_shot):
            query += f"and one_shot != {OneShot.EXCLUDE.value} "
        else:
            query += f"and one_shot != {OneShot.ONLY.value} "

        if self.lgbtq > Identity.NONE.flag:
            query += "and ((lgbtq & ?) > 0 or lgbtq = 0) "
            params.append(self.lgbtq)
        else:
            query += "and lgbtq = 0 "

        if self.age_limit == AgeLimit.NONE.value:
            query += f"and age_limit <= {AgeLimit.NONE.value} "
        elif self.age_limit == AgeLimit.OVER_18.value:
            query += f"and age_limit >= {AgeLimit.NONE.value} "
        elif self.age_limit == AgeLimit.OVER_21.value:
            query += f"and (age_limit = {AgeLimit.NONE.value} or age_limit = {AgeLimit.OVER_21.value}) "

        if self.vtt:
            query += "and ((vtt & ?) > 0 or vtt = 0) "
            params.append(self.vtt)

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

        if self.match_no_timezone and self.timezone:
            self.timezone.add("NOTZ")
        params.append(','.join(self.timezone) if self.timezone else None)

        if self.match_no_day and self.day:
            self.day.add("NODAY")
        params.append(','.join(self.day) if self.day else None)

        params.append(self.nsfw)
        params.append(self.keyword)
        params.append(self.flair)
        params.append(self.online)
        params.append(self.play_by_post)
        params.append(self.one_shot)
        params.append(self.lgbtq)
        params.append(self.age_limit)
        params.append(self.vtt)
        params.append(self.username)

        if self.exists(db):
            db.save("UPDATE user SET date_updated = CURRENT_TIMESTAMP, game = ?, timezone = ?, day = ?, nsfw = ?, keyword = ?, flair = ?, online = ?, play_by_post = ?, one_shot = ?, lgbtq = ?, age_limit = ?, vtt = ? WHERE username = ?", params)
        else:
            db.save("INSERT INTO user (game, timezone, day, nsfw, keyword, flair, online, play_by_post, one_shot, lgbtq, age_limit, vtt, username) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)

    def delete(self, db: Database) -> None:
        if self.username is not None:
            db.save("DELETE FROM user WHERE username = ?", [self.username])

    def update_notification_count(self, db: Database) -> None:
        db.save("UPDATE user SET notification_count = notification_count + 1 WHERE username = ?", [self.username])
