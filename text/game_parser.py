import re

__game_regex = re.compile(r"(CoC|3.5|[3-5]e|PF[1-2]e|BitD|BRP|CofD|Cyberpunk|DLC|DLR|DCC|DW|ODND|ADND|BX|DND2e|Earthdawn|Fate|Feast|FWS|GURPS|L5R|MCC|MotW|MM3|Numenera|SWADE|SWD|SR[3-6]|Starfinder|SWRPG|SWN|40K|WoD)", flags=re.IGNORECASE)

def parse_game(text):
    return set([i.upper() for i in re.findall(__game_regex, text)])
    