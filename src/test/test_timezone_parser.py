import pytest
from service.timezone_parser import timezone_to_gmt, parse_timezone


timezone_data = [
    ("PST", "GMT-8"),
    ("GMT+5", "GMT+5"),
    ("GMT-5", "GMT-5"),
    ("GMT +5", "GMT+5"),
    ("GMT+5:30", "GMT+5:30"),
    ("UTC+5", "GMT+5"),
    ("UTC-5", "GMT-5"),
    ("GMT +5", "GMT+5"),
    ("GMT +05", "GMT+5"),
    ("GMT+530", "GMT+5:30")
]


@pytest.mark.parametrize("text,output", timezone_data)
def test_timezone_to_gmt(text, output):
    assert timezone_to_gmt(text) == output


text_data = [
    ("PST", {"PST"}),
    ("GMT+5", {"GMT+5"}),
    ("GMT-5", {"GMT-5"}),
    ("GMT +5", {"GMT +5"}),
    ("GMT+5:30", {"GMT+5:30"}),
    ("UTC+5", {"UTC+5"}),
    ("UTC-5", {"UTC-5"}),
    ("ast", {"AST"}),
    ("past", set()),
    ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.", set())
]


@pytest.mark.parametrize("text,output", text_data)
def test_parse_timezone(text, output):
    assert parse_timezone(text) == output
