import typing

from .constants import Location, AgeLimit, Vtt, Identity
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
            post.time = result[8]
            post.online = result[9]
            post.nsfw = bool(result[10])
            post.permalink = result[11]
            post.play_by_post = bool(result[12])
            post.one_shot = bool(result[13])
            post.lgbtq = result[14]
            post.age_limit = result[15]
            post.vtt = result[16]

            posts.append(post)
        return posts

    @classmethod
    def find_post_by_date_created_greater_than_and_no_flair(cls, db, date: str) -> list:
        results = db.query("SELECT * FROM post WHERE date_created >= ? and flair is null", [date])
        return cls.__parse_results(results)

    @classmethod
    def find_post_by_submission_id(cls, db, submission_id: str) -> list:
        results = db.query("SELECT * FROM post WHERE submission_id = ?", [submission_id])
        return cls.__parse_results(results)

    @classmethod
    def statistics(cls, db, date: str = '2021-05-20') -> dict:
        total_posts = db.query("SELECT count(id) FROM post WHERE date_created >= ?", [date])[0][0]
        nsfw = db.query("SELECT sum(nsfw = 0), sum(nsfw = 1) FROM post WHERE date_created >= ?", [date])[0]
        location = db.query("SELECT sum(online = ?), sum(online = ?), sum(online = ?) FROM post WHERE date_created >= ?", [Location.ONLINE.value, Location.ONLINE_AND_OFFLINE.value, Location.OFFLINE.value, date])[0]
        pbp = db.query("SELECT sum(play_by_post = 1) FROM post WHERE date_created >= ?", [date])[0][0]
        one_shot = db.query("SELECT sum(one_shot = 1) FROM post WHERE date_created >= ?", [date])[0][0]
        identity = db.query("SELECT sum(lgbtq & ? > 0), sum(lgbtq & ? > 0), sum(lgbtq & ? > 0), sum(lgbtq & ? > 0) FROM post WHERE date_created >= ?", [Identity.LGBTQ.flag, Identity.FEM.flag, Identity.POC.flag, Identity.ACCESSIBLE.flag, date])[0]
        vtt = db.query("SELECT sum(vtt & ? > 0), sum(vtt & ? > 0), sum(vtt & ? > 0), sum(vtt & ? > 0), sum(vtt & ? > 0), sum(vtt & ? > 0), sum(vtt & ? > 0) FROM post WHERE date_created >= ?", [Vtt.ROLL20.flag, Vtt.FOUNDRY.flag, Vtt.FANTASY_GROUNDS.flag, Vtt.TABLETOP_SIM.flag, Vtt.ASTRAL.flag, Vtt.TALESPIRE.flag, Vtt.TABLEPLOP.flag, date])[0]
        day = db.query("SELECT sum(day like '%MONDAY%'),sum(day like '%TUESDAY%'),sum(day like '%WEDNESDAY%'),sum(day like '%THURSDAY%'),sum(day like '%FRIDAY%'),sum(day like '%SATURDAY%'),sum(day like '%SUNDAY%') FROM post WHERE date_created >= ?", [date])[0]
        flair = db.query("SELECT sum(flair='GM and player(s) wanted'), sum(flair='Player(s) wanted'), sum(flair='GM wanted') FROM post WHERE date_created >= ?", [date])[0]
        dnd = db.query("SELECT sum(game like '%5E%'), sum(game like '%4E%'), sum(game like '%3.5%'), sum(game like '%3E%'), sum(game like '%DND2E%'), sum(game like '%BX%'), sum(game like '%ADND%'), sum(game like '%ODND%') FROM post WHERE date_created >= ?", [date])[0]
        pf = db.query("SELECT sum(game like '%PF2E%'), sum(game like '%PF1E%') FROM post WHERE date_created >= ?", [date])[0]
        sr = db.query("SELECT sum(game like '%SR6%'), sum(game like '%SR5%'), sum(game like '%SR4%'), sum(game like '%SR3%') FROM post WHERE date_created >= ?", [date])[0]
        a_to_c = db.query("SELECT sum(game like '%40K%'), sum(game like '%BITD%'), sum(game like '%BRP%'), sum(game like '%COC%'), sum(game like '%COFD%'), sum(game like '%CYBERPUNK%') FROM post WHERE date_created >= ?", [date])[0]
        d_to_e = db.query("SELECT sum(game like '%DLC%'), sum(game like '%DLR%'), sum(game like '%DCC%'), sum(game like '%DW%'), sum(game like '%EARTHDAWN%') FROM post WHERE date_created >= ?", [date])[0]
        f_to_g = db.query("SELECT sum(game like '%FATE%'), sum(game like '%FEAST%'), sum(game like '%FLEXIBLE%'), sum(game like '%FWS%'), sum(game like '%GURPS%') FROM post WHERE date_created >= ?", [date])[0]
        h_to_n = db.query("SELECT sum(game like '%L5R%'), sum(game like '%MCC%'), sum(game like '%MOTW%'), sum(game like '%MM3%'), sum(game like '%NUMENERA%') FROM post WHERE date_created >= ?", [date])[0]
        o_to_z = db.query("SELECT sum(game like '%SWADE%'), sum(game like '%SWN%'), sum(game like '%STARFINDER%'), sum(game like '%SWRPG%'), sum(game like '%SWD%'), sum(game like '%WOD%') FROM post WHERE date_created >= ?", [date])[0]

        america = db.query("SELECT sum(timezone like '%GMT-4%'), sum(timezone like '%GMT-5%'), sum(timezone like '%GMT-6%'), sum(timezone like '%GMT-7%'), sum(timezone like '%GMT-8%'), sum(timezone like '%GMT-3%'), sum(timezone like '%GMT-9%') FROM post WHERE date_created >= ?", [date])[0]
        europe = db.query("SELECT sum(timezone like '%GMT-1%' and timezone not like '%GMT-10%'), sum(timezone like '%GMT+0%'), sum(timezone like '%GMT+1%' and timezone not like '%GMT+10%'  and timezone not like '%GMT+11%'), sum(timezone like '%GMT+2%'), sum(timezone like '%GMT+3%') FROM post WHERE date_created >= ?", [date])[0]
        aus = db.query("SELECT sum(timezone like '%GMT+8%'),  sum(timezone like '%GMT+9%' and timezone not like '%GMT+9:%'), sum(timezone like '%GMT+9:30%'), sum(timezone like '%GMT+10%' and timezone not like '%GMT+10:%'), sum(timezone like '%GMT+10:30%'), sum(timezone like '%GMT+11%') FROM post WHERE date_created >= ?", [date])[0]
        return {
            "data_start_date": date,
            "total_posts": total_posts,
            "nsfw_status": {
                "sfw": nsfw[0],
                "nsfw": nsfw[1]
            },
            "flair": {
                "gmplw": flair[0],
                "plw": flair[1],
                "gmw": flair[2]
            },
            "location": {
                "online": location[0],
                "online_and_offline": location[1],
                "offline": location[2]
            },
            "play_by_post": pbp,
            "one_shot": one_shot,
            "identity": {
                "lfbtq": identity[0],
                "fem": identity[1],
                "poc": identity[2],
                "accessible": identity[3],
            },
            "vtt": {
                "roll20": vtt[0],
                "foundry": vtt[1],
                "fantasy_grounds": vtt[2],
                "tabletop_simulator": vtt[3],
                "astral_tabletop": vtt[4],
                "talespire": vtt[5],
                "tableplop": vtt[6]
            },
            "day_of_week": {
                "monday": day[0],
                "tuesday": day[1],
                "wednesday": day[2],
                "thursday": day[3],
                "friday": day[4],
                "saturday": day[5],
                "sunday": day[6],
            },
            "game": {
                "40k": a_to_c[0],
                "bitd": a_to_c[1],
                "brp": a_to_c[2],
                "coc": a_to_c[3],
                "cofd": a_to_c[4],
                "cyberpunk": a_to_c[5],
                "dlc": d_to_e[0],
                "dlr": d_to_e[1],
                "dcc": d_to_e[2],
                "dw": d_to_e[3],
                "odnd": dnd[7],
                "adnd": dnd[6],
                "bx": dnd[5],
                "dnd2e": dnd[4],
                "3e": dnd[3],
                "3.5": dnd[2],
                "4e": dnd[1],
                "5e": dnd[0],
                "earthdawn": d_to_e[4],
                "fate": f_to_g[0],
                "feast": f_to_g[1],
                "flexible": f_to_g[2],
                "fws": f_to_g[3],
                "gurps": f_to_g[4],
                "l5r": h_to_n[0],
                "mcc": h_to_n[1],
                "motw": h_to_n[2],
                "mm3": h_to_n[3],
                "numenera": h_to_n[4],
                "pf2e": pf[0],
                "pf1e": pf[1],
                "swade": o_to_z[0],
                "swd": o_to_z[1],
                "sr3": sr[3],
                "sr4": sr[2],
                "sr5": sr[1],
                "sr6": sr[0],
                "starfinder": o_to_z[2],
                "swrpg": o_to_z[3],
                "swn": o_to_z[4],
                "wod": o_to_z[5],
            },
            "timezone": {
                "americas": {
                    "GMT-3": america[5],
                    "GMT-4": america[0],
                    "GMT-5": america[1],
                    "GMT-6": america[2],
                    "GMT-7": america[3],
                    "GMT-8": america[4],
                    "GMT-9": america[6],
                },
                "europe": {
                    "GMT-1": europe[0],
                    "GMT+0": europe[1],
                    "GMT+1": europe[2],
                    "GMT+2": europe[3],
                    "GMT+3": europe[4],
                },
                "australia": {
                    "GMT+8": aus[0],
                    "GMT+9": aus[1],
                    "GMT+9:30": aus[2],
                    "GMT+10": aus[3],
                    "GMT+10:30": aus[4],
                    "GMT+11": aus[5],
                }
            }
        }

    def __init__(self, **kwargs):
        self.id: int = kwargs.get("id", None)
        self.date_created: str = kwargs.get("date_created", None)
        self.date_updated: str = kwargs.get("date_updated", None)
        self.submission_id: str = kwargs.get("submission_id", None)
        self.flair: str = kwargs.get("flair", None)
        self.game: typing.Set[str] = kwargs.get("game", set())
        self.day: typing.Set[str] = kwargs.get("day", set())
        self.timezone: typing.Set[str] = kwargs.get("timezone", set())
        self.time: str = kwargs.get("time", None)
        self.online: int = kwargs.get("online", Location.NONE.value)
        self.nsfw: bool = kwargs.get("nsfw", False)
        self.permalink: str = kwargs.get("permalink", None)
        self.play_by_post: bool = kwargs.get("play_by_post", False)
        self.one_shot: bool = kwargs.get("one_shot", False)
        self.lgbtq: int = kwargs.get("lgbtq", Identity.NONE.value)
        self.age_limit: int = kwargs.get("age_limit", AgeLimit.NONE.value)
        self.vtt: int = kwargs.get("vtt", Vtt.NONE.flag)

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
        params.append(self.time)
        params.append(self.online)
        params.append(int(self.nsfw))
        params.append(self.permalink)
        params.append(int(self.play_by_post))
        params.append(int(self.one_shot))
        params.append(self.lgbtq)
        params.append(self.age_limit)
        params.append(self.vtt)
        db.save("INSERT INTO post (submission_id, flair, game, day, timezone, time, online, nsfw, permalink, play_by_post, one_shot, lgbtq, age_limit, vtt) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)

    def flags_as_string_list(self) -> list:
        flags = []
        self.nsfw and flags.append("Nsfw")
        self.play_by_post and flags.append("Play-by-Post")
        self.one_shot and flags.append("One-Shot")

        flags.extend(Identity.flag_to_str_array(self.lgbtq))
        if limit := AgeLimit.tostring(int(self.age_limit)):
            flags.append(limit)
        flags.extend(Vtt.flag_to_str_array(self.vtt))
        return flags
