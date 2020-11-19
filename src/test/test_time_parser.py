import pytest
from service.time_parser import parse_time, to_military_time


no_time_data = [
    ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
    ("2009"),
    ("1492"),
    ("2400"),
    ("12"),
    ("18+"),
    ("5e"),
    ("3-4"),
    ("3 - 4"),
    ("3 to 4"),
    ("10 amx"),
    ("10 ax"),
    ("12 px"),
    ("12 pmx"),
    ("xyz0000#")
]


@pytest.mark.parametrize("text", no_time_data)
def test_parse_time_no_time(text):
    assert parse_time(text) == (None, None)


to_military_time_data = [
    ("7", "a", "0700"),
    ("7", "p", "1900"),
    ("7.30", "p", "1930"),
    ("7:30", "p", "1930"),
    ("0700", "a", "0700"),
    ("700", "p", "1900"),
    ("700", "a", "0700"),
    ("715", "a", "0715"),
    ("730", "a", "0730"),
    ("745", "a", "0745"),
    ("12", "a", "0000"),
    ("12", "p", "1200"),
    ("10", "p", "2200")
]


@pytest.mark.parametrize("text,period,result", to_military_time_data)
def test_to_military_time(text, period, result):
    assert to_military_time(text, period) == result


military_time_data = [
    ("noon", "1200", None),
    ("midnight", "0000", None),
    ("0000", "0000", None),
    ("0700", "0700", None),
    ("0715", "0715", None),
    ("0730", "0730", None),
    ("0745", "0745", None),
    ("1100", "1100", None),
    ("2200", "2200", None),
    ("2300", "2300", None),
    ("23:00", "2300", None),
    ("0100-2345", "0100", "2345"),
    ("0100 - 2345", "0100", "2345"),
    ("0100to2345", "0100", "2345"),
    ("0100 to 2345", "0100", "2345"),
    ("Lorem ipsum 0700 dolor sit amet", "0700", None),
    ("Lorem ipsum 0100 to 2345 dolor sit amet", "0100", "2345"),
    ("[1900-2300]", "1900", "2300")
]


@pytest.mark.parametrize("text,start_time,end_time", military_time_data)
def test_parse_time_input_military_time(text, start_time, end_time):
    assert parse_time(text) == (start_time, end_time)


double_period_time_data = [
    ("7a", "0700", None),
    ("7p", "1900", None),
    ("7.30pm", "1930", None),
    ("0700am", "0700", None),
    ("700am", "0700", None),
    ("715am", "0715", None),
    ("730am", "0730", None),
    ("745am", "0745", None),
    ("10a", "1000", None),
    ("10 a ", "1000", None),
    ("10am", "1000", None),
    ("10 am", "1000", None),
    ("12 am", "0000", None),
    ("12 pm", "1200", None),
    ("10p", "2200", None),
    ("10 p ", "2200", None),
    ("10pm", "2200", None),
    ("10 pm", "2200", None),
    ("[10pm]", "2200", None),
    ("7:00 AM - 12:00 AM", "0700", "0000"),
    ("10:00 PM - 12:00 AM", "2200", "0000"),
    ("0700 PM - 1200 AM", "1900", "0000"),
    ("700 PM - 1200 AM", "1900", "0000"),
    ("7:00 P.M - 12:00 A.M", "1900", "0000"),
    ("7:00 P.M. - 12:00 A.M.", "1900", "0000"),
    ("7:00 PM. - 12:00 AM.", "1900", "0000"),
    ("7:00 PM-12:00 AM", "1900", "0000"),
    ("7:00PM - 12:00AM", "1900", "0000"),
    ("7:00PM-12:00AM", "1900", "0000"),
    ("7 PM - 12 AM", "1900", "0000"),
    ("7PM - 12AM", "1900", "0000"),
    ("7PM-12AM", "1900", "0000"),
    ("7p-12a", "1900", "0000"),
    ("7pm to 12am", "1900", "0000"),
    ("07pm-12am", "1900", "0000"),
    ("07 pm - 12 am", "1900", "0000"),
    ("7.30 pm - 12 am", "1930", "0000"),
    ("[7pm-12am]", "1900", "0000")
]


@pytest.mark.parametrize("text,start_time,end_time", double_period_time_data)
def test_parse_time_input_double_period_time(text, start_time, end_time):
    assert parse_time(text) == (start_time, end_time)


single_period_time_data = [
    ("noon to 6pm", "1200", "1800"),
    ("midnight to 6am", "0000", "0600"),
    ("7:00 - 11:00 AM.", "0700", "1100"),
    ("7:00 - 11:00 A.M.", "0700", "1100"),
    ("7-11a", "0700", "1100"),
    ("2-7am", "0200", "0700"),
    ("2-7pm", "1400", "1900"),
    ("2 to 7pm", "1400", "1900"),
    ("2.30 - 7 pm", "1430", "1900"),
    ("11-1pm", "1100", "1300"),
    ("10-1am", "2200", "0100"),
    ("[7-12am]", "1900", "0000")
]


@pytest.mark.parametrize("text,start_time,end_time", single_period_time_data)
def test_parse_time_input_single_period_time(text, start_time, end_time):
    assert parse_time(text) == (start_time, end_time)
