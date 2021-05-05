import re

from model import Flair


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
        if match[0] == '=':
            return -1
        else:
            return 0
    return 1


def is_lgbt(text: str) -> bool:
    return bool(text and re.search(r"lgbtq?[+]?", text, re.IGNORECASE))


def age_limit(text: str) -> str:
    match = re.search(r"(?:18|19|20|21)[+]", text, re.IGNORECASE)
    return match.group(0) if match else None


def is_one_shot(text: str) -> bool:
    return bool(text and re.search(r"one[-\s]shot", text, re.IGNORECASE))


def is_play_by_post(text: str) -> bool:
    return bool(text and re.search(r"play[-\s]by[-\s]post|pbp", text, re.IGNORECASE))


def find_all_keyword(text: str) -> list:
    matches = re.findall(r"\[(.*?)\]", text)
    return matches


def using_vtt(text: str) -> str:
    match = re.search(r"(roll\s?20|r20)|(fantasy ground)|(tabletop sim)|(foundry vtt)", text, flags=re.IGNORECASE)
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
