import re

def players_wanted(text):
    return 1 if re.search(r"(Player\(s\)\swanted)", text, re.IGNORECASE) else 0

def is_nsfw(text):
    return 1 if re.search(r"nsfw", text, re.IGNORECASE) else 0

def is_online(text):
    return 1 if re.search(r"online", text, re.IGNORECASE) else 0

def is_offline(text):
    return 1 if re.search(r"offline", text, re.IGNORECASE) else 0

def is_lgbt(text):
    return 1 if re.search(r"lgbtq?[+]?", text, re.IGNORECASE) else 0

def is_over_18(text):
    return 1 if re.search(r"(18|21)[+]", text, re.IGNORECASE) else 0

def is_one_shot(text):
    return 1 if re.search(r"one[-\s]shot", text, re.IGNORECASE) else 0