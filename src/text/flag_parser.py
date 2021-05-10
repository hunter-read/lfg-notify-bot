import re

from model import Flair, Location, Nsfw, PlayByPost, OneShot, Lgbtq, AgeLimit, Vtt


__play_by_post = r"(play[-\s]by[-\s]post|pbp)"
__one_shot = r"one[-\s]?shot"
__lgbt = r"lgbtq?[+]?"


def __using_vtt(text: str) -> int:
    flag = Vtt.NONE.flag
    matches = re.finditer(r"(roll\s?20|r20)|(fantasy ground|fg)|(tabletop sim|tts)|(foundry)", text, flags=re.IGNORECASE)
    for match in matches:
        if match:
            if match.group(1):
                flag |= Vtt.ROLL20.flag
            elif match.group(2):
                flag |= Vtt.FANTASY_GROUNDS.flag
            elif match.group(3):
                flag |= Vtt.TABLETOP_SIM.flag
            elif match.group(4):
                flag |= Vtt.FOUNDRY.flag
    return flag


def __age_limit(text: str) -> str:
    match = re.search(r"(((18|19|20|21)[+])|anyage)", text, re.IGNORECASE)
    if match:
        if match.group(1).startswith("18"):
            return AgeLimit.OVER_18
        elif match.group(1).lower() == "anyage":
            return AgeLimit.ANY_AGE
        else:
            return AgeLimit.OVER_21
    return AgeLimit.NONE


def parse_flair(text: str) -> int:
    flair = 0
    if not text:
        return flair
    matches = re.finditer(r"(gm\sand\splayer\(?s?\)?\swanted|gmplw)|(player\(?s?\)?\swanted|plw)|(gm\swanted|gmw)", text, re.IGNORECASE)
    for match in matches:
        if match.group(1):
            flair |= Flair.GM_AND_PLAYERS_WANTED.flag
        elif match.group(2):
            flair |= Flair.PLAYERS_WANTED.flag
        elif match.group(3):
            flair |= Flair.GM_WANTED.flag
    return flair


def parse_location(text: str) -> int:
    if not text:
        return Location.NONE

    online = re.search(r"online", text, re.IGNORECASE)
    offline = re.search(r"offline", text, re.IGNORECASE)
    if online and offline:
        return Location.ONLINE_AND_OFFLINE
    elif online:
        return Location.ONLINE
    elif offline:
        return Location.OFFLINE

    return Location.NONE


def parse_message_flags(text) -> dict:
    flags = {
        "location": Location.ONLINE,
        "nsfw": Nsfw.EXCLUDE,
        "pbp": PlayByPost.INCLUDE,
        "one_shot": OneShot.INCLUDE,
        "lgbtq": Lgbtq.INCLUDE,
        "age_limit": AgeLimit.NONE,
        "vtt": Vtt.NONE.flag
    }
    if not text:
        return flags

    if match := re.search(r"=?off(line)?", text, re.IGNORECASE):
        flags["location"] = Location.OFFLINE if match.group(0).startswith("=") else Location.ONLINE_AND_OFFLINE

    if match := re.search(r"=?nsfw", text, re.IGNORECASE):
        flags["nsfw"] = Nsfw.ONLY if match.group(0).startswith("=") else Nsfw.INCLUDE

    if pbp_match := re.search(rf"\-?{__play_by_post}", text, re.IGNORECASE):
        flags["pbp"] = PlayByPost.EXCLUDE if pbp_match.group(0).startswith("-") else PlayByPost.ONLY

    if os_match := re.search(rf"\-?{__one_shot}", text, re.IGNORECASE):
        flags["one_shot"] = OneShot.EXCLUDE if os_match.group(0).startswith("-") else OneShot.ONLY

    flags["lgbtq"] = Lgbtq.ONLY if re.search(rf"{__lgbt}", text, re.IGNORECASE) else Lgbtq.INCLUDE

    flags["age_limit"] = __age_limit(text)
    flags["vtt"] = __using_vtt(text)

    return flags


def parse_submission_flags(text) -> dict:
    flags = {
        "pbp": False,
        "one_shot": False,
        "lgbtq": False,
        "age_limit": AgeLimit.NONE,
        "vtt": Vtt.NONE
    }

    if not text:
        return flags

    flags["pbp"] = bool(re.search(rf"{__play_by_post}", text, re.IGNORECASE))
    flags["one_shot"] = bool(re.search(rf"{__one_shot}", text, re.IGNORECASE))
    flags["lgbtq"] = bool(re.search(rf"{__lgbt}", text, re.IGNORECASE))
    flags["age_limit"] = __age_limit(text)
    flags["vtt"] = __using_vtt(text)
    return flags


def find_all_keyword(text: str) -> list:
    matches = re.findall(r"\[(.*?)\]", text)
    return matches
