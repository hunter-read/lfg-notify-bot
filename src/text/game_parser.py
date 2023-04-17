import re
import typing


__game_dict = {
    "5E": "D&D 5th Edition",
    "3.5": "D&D 3.5 Edition",
    "PF2E": "Pathfinder 2nd Edition",
    "PF1E": "Pathfinder 1st Edition",
    "COC": "Call of Cthulhu",
    "CYBERPUNK": "Cyberpunk 2020",
    "40K": "Warhammer 40K",
    "WOD": "World of Darkness",
    "FLEXIBLE": "Flexible / Other",
    "BITD": "Blades in the Dark",
    "BRP": "Basic Role-Playing",
    "COFD": "Chronicles of Darkness",
    "DLC": "Deadlands Classics",
    "DLR": "Deadlands Reloaded",
    "DCC": "Dungeon Crawl Classics",
    "DW": "Dungeon World",
    "ODND": "D&D Original Edition",
    "ADND": "D&D Advanced",
    "BX": "D&D Basic/Expert",
    "DND2E": "D&D 2nd Edition",
    "3E": "D&D 3rd Edition",
    "4E": "D&D 4th Edition",
    "1DND": "One D&D",
    "EARTHDAWN": "Earthdawn",
    "FATE": "Fate Core",
    "FEAST": "Feast of Legends",
    "FWS": "Fellowship",
    "GURPS": "GURPS",
    "L5R": "Legend of the Five Rings",
    "MCC": "Monster Crawl Classics",
    "MOTW": "Monster of the Week",
    "MM3": "Mutants & Masterminds 3rd Edition",
    "NUMENERA": "Numenera",
    "SWADE": "Savage Worlds Adventure Edition",
    "SWD": "Savage Worlds Deluxe",
    "SR3": "Shadowrun 3rd Edition",
    "SR4": "Shadowrun 4th Edition",
    "SR5": "Shadowrun 5th Edition",
    "SR6": "Shadowrun 6th Edition",
    "STARFINDER": "Starfinder",
    "SWRPG": "Star Wars RPG",
    "SWN": "Stars Without Numbers",
}
__game_regex = re.compile(r"(CoC|3\.5|[3-5]e|PF[1-2]e|BitD|BRP|CofD|Cyberpunk|DLC|DLR|DCC|DW|ODND|ADND|BX|DND2e|1DND|Earthdawn|Fate|Feast|FWS|GURPS|L5R|MCC|MotW|MM3|Numenera|SWADE|SWD|SR[3-6]|Starfinder|SWRPG|SWN|40K|WoD|(?:(?:\[|<|\(|{)(?:Flexible|Other)(?:\]|>|\)|})))", flags=re.IGNORECASE)


def parse_game(text: str) -> typing.Set[str]:
    return set([i.upper() if ("other" not in i.lower() and 'flexible' not in i.lower()) else "FLEXIBLE" for i in re.findall(__game_regex, text)])


def game_abbreviation_to_string(text: str) -> str:
    return __game_dict.get(text, text)
