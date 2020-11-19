import re


def players_wanted(text: str) -> int:
    return 1 if re.search(r"(Player\(s\)\swanted)", text, re.IGNORECASE) else 0


def is_nsfw(text: str) -> int:
    return 1 if re.search(r"nsfw", text, re.IGNORECASE) else 0


def is_online(text: str) -> int:
    return 1 if re.search(r"online", text, re.IGNORECASE) else 0


def is_offline(text: str) -> int:
    return 1 if re.search(r"offline", text, re.IGNORECASE) else 0


def is_lgbt(text: str) -> int:
    return 1 if re.search(r"lgbtq?[+]?", text, re.IGNORECASE) else 0


def age_limit(text: str) -> str:
    match = re.search(r"(?:18|19|20|21)[+]", text, re.IGNORECASE)
    return match.group(0) if match else None


def is_one_shot(text: str) -> int:
    return 1 if re.search(r"one[-\s]shot", text, re.IGNORECASE) else 0