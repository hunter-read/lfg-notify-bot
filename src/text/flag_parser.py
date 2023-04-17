import re

from model import Flair, Location, Nsfw, PlayByPost, OneShot, Identity, AgeLimit, Vtt


__play_by_post = r"(play[-\s]by[-\s]post|pbp)"
__one_shot = r"one[-\s]?shot"


def __match_identity(text: str) -> int:
    flag = Identity.NONE.flag
    matches = re.finditer(r"(lgbtq?[+]?)|(\bfem\b)|(\bpoc\b)|(accessible)", text, flags=re.IGNORECASE)
    for match in matches:
        if match:
            if match.group(1):
                flag |= Identity.LGBTQ.flag
            elif match.group(2):
                flag |= Identity.FEM.flag
            elif match.group(3):
                flag |= Identity.POC.flag
            elif match.group(4):
                flag |= Identity.ACCESSIBLE.flag
    return flag


def __using_vtt(text: str) -> int:
    flag = Vtt.NONE.flag
    matches = re.finditer(r"(roll\s?20|r20)|(fantasy ground|fg)|(tabletop sim|tts)|(foundry)|(astral)|(tableplop)|(talespire)|(omm|one more multiverse)|(owlbear)|(above\s?vtt)", text, flags=re.IGNORECASE)
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
            elif match.group(5):
                flag |= Vtt.ASTRAL.flag
            elif match.group(6):
                flag |= Vtt.TABLEPLOP.flag
            elif match.group(7):
                flag |= Vtt.TALESPIRE.flag
            elif match.group(8):
                flag |= Vtt.ONE_MORE_MULTIVERSE.flag
            elif match.group(9):
                flag |= Vtt.OWLBEAR_RODEO.flag
            elif match.group(10):
                flag |= Vtt.ABOVE_VTT.flag
    return flag


def __age_limit(text: str) -> str:
    match = re.search(r"(((18|19|20|21)[+])|anyage)", text, re.IGNORECASE)
    if match:
        if match.group(1).startswith("18"):
            return AgeLimit.OVER_18.value
        elif match.group(1).lower() == "anyage":
            return AgeLimit.ANY_AGE.value
        else:
            return AgeLimit.OVER_21.value
    return AgeLimit.NONE.value


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
        return Location.NONE.value

    online = re.search(r"online", text, re.IGNORECASE)
    offline = re.search(r"offline", text, re.IGNORECASE)
    if online and offline:
        return Location.ONLINE_AND_OFFLINE.value
    elif online:
        return Location.ONLINE.value
    elif offline:
        return Location.OFFLINE.value

    return Location.NONE.value


def parse_message_flags(text) -> dict:
    flags = {
        "location": Location.ONLINE.value,
        "nsfw": Nsfw.EXCLUDE.value,
        "play_by_post": PlayByPost.INCLUDE.value,
        "one_shot": OneShot.INCLUDE.value,
        "lgbtq": Identity.NONE.flag,
        "age_limit": AgeLimit.NONE.value,
        "vtt": Vtt.NONE.flag,
        "match_no_timezone": False,
        "match_no_day": False
    }
    if not text:
        return flags

    if match := re.search(r"=?off(line)?", text, re.IGNORECASE):
        flags["location"] = (Location.OFFLINE if match.group(0).startswith("=") else Location.ONLINE_AND_OFFLINE).value

    if match := re.search(r"=?nsfw", text, re.IGNORECASE):
        flags["nsfw"] = (Nsfw.ONLY if match.group(0).startswith("=") else Nsfw.INCLUDE).value

    if pbp_match := re.search(rf"\-?{__play_by_post}", text, re.IGNORECASE):
        flags["play_by_post"] = (PlayByPost.EXCLUDE if pbp_match.group(0).startswith("-") else PlayByPost.ONLY).value

    if os_match := re.search(rf"\-?{__one_shot}", text, re.IGNORECASE):
        flags["one_shot"] = (OneShot.EXCLUDE if os_match.group(0).startswith("-") else OneShot.ONLY).value

    flags["lgbtq"] = __match_identity(text)
    flags["age_limit"] = __age_limit(text)
    flags["vtt"] = __using_vtt(text)
    flags["match_no_timezone"] = bool(re.search(r"no-?(tz|timezone)", text, re.IGNORECASE))
    flags["match_no_day"] = bool(re.search(r"no-?day", text, re.IGNORECASE))

    return flags


def parse_submission_flags(text) -> dict:
    flags = {
        "play_by_post": False,
        "one_shot": False,
        "lgbtq": Identity.NONE.flag,
        "age_limit": AgeLimit.NONE.value,
        "vtt": Vtt.NONE.value
    }

    if not text:
        return flags

    flags["play_by_post"] = bool(re.search(rf"{__play_by_post}", text, re.IGNORECASE))
    flags["one_shot"] = bool(re.search(rf"{__one_shot}", text, re.IGNORECASE))
    flags["lgbtq"] = __match_identity(text)
    flags["age_limit"] = __age_limit(text)
    flags["vtt"] = __using_vtt(text)
    return flags


def find_all_keyword(text: str) -> list:
    matches = re.findall(r"\[(.*?)\]", text)
    return matches
