import pytest
from service.flag_parser import using_vtt


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
