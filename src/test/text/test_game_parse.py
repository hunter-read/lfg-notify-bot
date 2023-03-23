import pytest

from text.game_parser import parse_game


game_data = [
    ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", set()),
    ("CoC", {"COC"}),
    ("3.5", {"3.5"}),
    ("3e", {"3E"}),
    ("4e", {"4E"}),
    ("5e", {"5E"}),
    ("PF1e", {"PF1E"}),
    ("PF2e", {"PF2E"}),
    ("BitD", {"BITD"}),
    ("BRP", {"BRP"}),
    ("CofD", {"COFD"}),
    ("Cyberpunk", {"CYBERPUNK"}),
    ("DLC", {"DLC"}),
    ("DLR", {"DLR"}),
    ("DCC", {"DCC"}),
    ("DW", {"DW"}),
    ("ODND", {"ODND"}),
    ("ADND", {"ADND"}),
    ("BX", {"BX"}),
    ("DND2e", {"DND2E"}),
    ("Earthdawn", {"EARTHDAWN"}),
    ("Fate", {"FATE"}),
    ("Feast", {"FEAST"}),
    ("FWS", {"FWS"}),
    ("GURPS", {"GURPS"}),
    ("L5R", {"L5R"}),
    ("MCC", {"MCC"}),
    ("MotW", {"MOTW"}),
    ("MM3", {"MM3"}),
    ("Numenera", {"NUMENERA"}),
    ("SWADE", {"SWADE"}),
    ("SWD", {"SWD"}),
    ("SR3", {"SR3"}),
    ("SR4", {"SR4"}),
    ("SR5", {"SR5"}),
    ("SR6", {"SR6"}),
    ("Starfinder", {"STARFINDER"}),
    ("SWRPG", {"SWRPG"}),
    ("SWN", {"SWN"}),
    ("40K", {"40K"}),
    ("WoD", {"WOD"}),
    ("3e, 4e 5e", {"3E", "4E", "5E"}),
    ("3-5", set()),
    ("other", set()),
    ("(other)", {"FLEXIBLE"}),
    ("[other]", {"FLEXIBLE"}),
    ("<OTHER>", {"FLEXIBLE"}),
    ("{other}", {"FLEXIBLE"}),
    ("flexible", set()),
    ("(flexible)", {"FLEXIBLE"}),
    ("<Flexible>", {"FLEXIBLE"}),
    ("{Flexible}", {"FLEXIBLE"}),
    ("[FLEXIBLE]", {"FLEXIBLE"})
]


@pytest.mark.parametrize("text,game", game_data)
def test_parse_game(text, game):
    assert parse_game(text) == game
