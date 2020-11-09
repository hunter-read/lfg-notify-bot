import pytest
from service.day_parser import parse_day


no_day_data = [
    ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
    ("montreal"),
    ("no"),
    ("pst"),
    ("5e")
]


@pytest.mark.parametrize("text", no_day_data)
def test_parse_no_day(text):
    assert not parse_day(text)


day_data = [
    ("monday", {"MONDAY"}),
    ("Tuesday", {"TUESDAY"}),
    ("wednesDay", {"WEDNESDAY"}),
    ("Lorem ipsum thursday dolor sit amet", {"THURSDAY"}),
    ("friday, saturdays, sundays", {"SUNDAY", "FRIDAY", "SATURDAY"}),
    ("mon", {"MONDAY"}),
    ("tue", {"TUESDAY"}),
    ("tues", {"TUESDAY"}),
    ("wed", {"WEDNESDAY"}),
    ("thu", {"THURSDAY"}),
    ("thur", {"THURSDAY"}),
    ("thurs", {"THURSDAY"}),
    ("fri", {"FRIDAY"}),
    ("sat", {"SATURDAY"}),
    ("sun", {"SUNDAY"}),
    ("weekends", {"SUNDAY", "SATURDAY"}),
    ("weekdays", {"MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"})
]


@pytest.mark.parametrize("text,result", day_data)
def test_parse_day(text, result):
    assert parse_day(text) == result
