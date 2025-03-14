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
    "DCC": "Dungeon Crawl Classics",
    "DW": "Dungeon World",
    "ODND": "D&D Original Edition",
    "ADND": "D&D Advanced",
    "BX": "D&D Basic/Expert",
    "DND2E": "D&D 2nd Edition",
    "3E": "D&D 3rd Edition",
    "4E": "D&D 4th Edition",
    "5E 2024": "D&D 5th Edition (2024)",
    "FATE": "Fate Core",
    "GURPS": "GURPS",
    "MOTW": "Monster of the Week",
    "MM3": "Mutants & Masterminds 3rd Edition",
    "NUMENERA": "Numenera",
    "OSR": "Old School Renaissance",
    "SAVAGEWORLDS": "Savage Worlds",
    "SHADOWRUN": "Shadowrun (Any Edition)",
    "STARFINDER": "Starfinder",
    "SWRPG": "Star Wars RPG",
    "SWN": "Stars Without Numbers",
    # deprecated
    "1DND": "One D&D",
    "DLC": "Deadlands Classics",
    "DLR": "Deadlands Reloaded",
    "EARTHDAWN": "Earthdawn",
    "FEAST": "Feast of Legends",
    "FWS": "Fellowship",
    "L5R": "Legend of the Five Rings",
    "MCC": "Monster Crawl Classics",
    "SWADE": "Savage Worlds Adventure Edition",
    "SWD": "Savage Worlds Deluxe",
    "SR3": "Shadowrun 3rd Edition",
    "SR4": "Shadowrun 4th Edition",
    "SR5": "Shadowrun 5th Edition",
    "SR6": "Shadowrun 6th Edition"
}
__game_regex = re.compile(
    r"(CoC|3\.5|[3-5]e|PF[1-2]e|BitD|BRP|CofD|Cyberpunk|DLC|DLR|DCC|DW|ODND|ADND|BX|DND2e|1DND|5\.5|Earthdawn|Fate|Feast|FWS|GURPS|L5R|MCC|MotW|MM3|Numenera|SWADE|SWD|SR[3-6]|Starfinder|SWRPG|SWN|40K|WoD|OSR|Shadowrun|SavageWorlds|(?:(?:\[|<|\(|{)(?:Flexible|Other)(?:\]|>|\)|})))",
    flags=re.IGNORECASE,
)
__dnd_14regex = re.compile(r"(14/24|24/14|2014)", flags=re.IGNORECASE)
__dnd_24regex = re.compile(r"(2024|'24|5e\.?\s?24|14/24|24/14)", flags=re.IGNORECASE)


def parse_game(text: str) -> typing.Set[str]:
    games = set(
        [
            i.upper() if ("other" not in i.lower() and "flexible" not in i.lower()) else "FLEXIBLE"
            for i in re.findall(__game_regex, text)
        ]
    )
    if "5E" in games:
        dnd14 = re.search(__dnd_14regex, text)
        dnd24 = re.search(__dnd_24regex, text)
        if dnd24:
            games.add("5E 2024")
            if not dnd14:
                games.remove("5E")

    dnd24 = {"1DND", "5.5"}
    if not dnd24.isdisjoint(games):
        games.add("5E 2024")
        games.discard("1DND")
        games.discard("5.5")

    deprecated_games = {"DLR", "DLC", "EARTHDAWN", "FEAST", "FWS", "L5R", "MCC"}
    if not deprecated_games.isdisjoint(games):
        games.add("FLEXIBLE")

    shadowrun = {"SR3", "SR4", "SR5", "SR6"}
    if not shadowrun.isdisjoint(games):
        games.add("SHADOWRUN")

    savage = {"SWADE", "SWD"}
    if not savage.isdisjoint(games):
        games.add("SAVAGEWORLDS")

    return games


def game_abbreviation_to_string(text: str) -> str:
    return __game_dict.get(text, text)
