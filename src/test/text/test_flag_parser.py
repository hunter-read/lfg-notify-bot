import pytest

from text.flag_parser import using_vtt, parse_flair


vtt_data = [
    ("r20", "Roll20"),
    ("roll20", "Roll20"),
    ("roll 20", "Roll20"),
    ("Hello roll 20 World", "Roll20"),
    ("foundry vtt", "Foundry VTT"),
    ("foundry", None),
    ("tabletop simulator", "Tabletop Simulator"),
    ("tabletop sim", "Tabletop Simulator"),
    ("fantasy grounds", "Fantasy Grounds"),
    ("Hello World!", None)
]


@pytest.mark.parametrize("text,result", vtt_data)
def test_parse_vtt(text, result):
    assert using_vtt(text) == result


flair_data = [
    (None, 0),
    ("Player(s) wanted", 1),
    ("GM and player(s) wanted", 2),
    ("GM wanted", 4),
    ("GM and player(s) wanted, Player(s) wanted", 3),
    ("GM and player(s) wanted, Player(s) wanted, GM wanted", 7),
    ("Meta", 0)
]


@pytest.mark.parametrize("text,result", flair_data)
def test_parse_flair(text, result):
    assert parse_flair(text) == result
