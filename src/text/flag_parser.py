import re

from model import Flair


__play_by_post = r"play[-\s]by[-\s]post|pbp"
__one_shot = r"one[-\s]shot"
__lgbt = r"lgbtq?[+]?"
__roll20 = r"(roll\s?20|r20)"


def parse_flair(text: str) -> int:
    flair = 0
    if not text:
        return flair
    matches = re.findall(r"GM\sand\splayer\(?s?\)?\swanted|player\(?s?\)?\swanted|gm\swanted|gmplw|gmw|plw", text, re.IGNORECASE)
    for match in matches:
        if re.search(r"GM\sand\splayer\(?s?\)?\swanted|gmplw", match, re.IGNORECASE):
            flair |= Flair.GM_AND_PLAYERS_WANTED.flag
        elif re.search(r"player\(?s?\)?\swanted|plw", match, re.IGNORECASE):
            flair |= Flair.PLAYERS_WANTED.flag
        elif re.search(r"gm\swanted|gmw", match, re.IGNORECASE):
            flair |= Flair.GM_WANTED.flag
    return flair


def is_nsfw(text: str) -> bool:
    return bool(text and re.search(r"nsfw", text, re.IGNORECASE))


def is_online(text: str) -> bool:
    return bool(text and re.search(r"online", text, re.IGNORECASE))


def is_offline(text: str) -> bool:
    return bool(text and re.search(r"offline", text, re.IGNORECASE))


def determine_online_or_offline(text: str) -> int:
    match = re.search(r"=?off(line)?", text, re.IGNORECASE)
    if match:
        if "=" in match[0]:
            return -1
        else:
            return 0
    return 1


def is_lgbt(text: str) -> bool:
    return bool(text and re.search(rf"{__lgbt}", text, re.IGNORECASE))


def age_limit(text: str) -> str:
    match = re.search(r"(?:18|21)[+]", text, re.IGNORECASE)
    return match.group(0) if match else None


def is_one_shot(text: str) -> bool:
    return bool(text and re.search(rf"{__one_shot}", text, re.IGNORECASE))


def is_play_by_post(text: str) -> bool:
    return bool(text and re.search(rf"{__play_by_post}", text, re.IGNORECASE))


def find_all_keyword(text: str) -> list:
    matches = re.findall(r"\[(.*?)\]", text)
    return matches


def using_vtt(text: str) -> str:
    match = re.search(rf"{__roll20}|(fantasy ground)|(tabletop sim)|(foundry vtt)", text, flags=re.IGNORECASE)
    if match:
        if match.group(1):
            return "Roll20"
        elif match.group(2):
            return "Fantasy Grounds"
        elif match.group(3):
            return "Tabletop Simulator"
        elif match.group(4):
            return "Foundry VTT"
    return None


def parse_message_flags(text) -> list:
    pbp = 0
    if pbp_match := re.search(rf"(\-?{__play_by_post})", text, re.IGNORECASE):
        pbp = 1 if pbp_match.group(0).startswith("-") else 0
    one_shot = 0
    if os_match := re.search(rf"(\-?{__one_shot})", text, re.IGNORECASE):
        one_shot = 1 if os_match.group(0).startswith("-") else 0
    lgbt = 1 if re.searh(rf"{__lgbt}", text, re.IGNORECASE) else 0
    # TODO: age
    # TODO: VTT
    # TODO: ADD TESTING!!!!!

    return [pbp, one_shot, lgbt]
