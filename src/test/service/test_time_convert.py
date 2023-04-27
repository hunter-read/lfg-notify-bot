import pytest

from service.time_convert import to_gmt, to_timezone, convert_time_across_timezones


to_gmt_data = [
    ("1200", "GMT-8", "2000"),
    ("1200", "GMT+8", "0400"),
    ("0400", "GMT+8", "2000-"),
    ("2000", "GMT-8", "0400+"),
    ("0400", "GMT+4", "0000"),
    ("2000", "GMT-4", "0000+"),
    ("1200", "GMT+0", "1200"),
    ("1200", "GMT-10:30", "2230"),
    ("1200", "GMT+10:30", "0130"),
]


@pytest.mark.parametrize("time,timezone,result", to_gmt_data)
def test_to_gmt(time, timezone, result):
    assert to_gmt(time, timezone) == result


to_timezone_data = [
    ("2000", "GMT-8", "1200"),
    ("0400", "GMT+8", "1200"),
    ("2000", "GMT+8", "0400+"),
    ("2000", "GMT+4", "0000+"),
    ("0400", "GMT-4", "0000"),
    ("1200", "GMT+0", "1200"),
    ("2230", "GMT-10:30", "1200"),
    ("0130", "GMT+10:30", "1200"),
]


@pytest.mark.parametrize("time,timezone,result", to_timezone_data)
def test_to_timezone(time, timezone, result):
    assert to_timezone(time, timezone) == result


convert_across_timezone_data = [
    ("1200", "GMT+0", "GMT+0", "1200"),
    ("2000", "GMT-8", "GMT-8", "2000"),
    ("0400", "GMT+8", "GMT+8", "0400"),
    ("0400", "GMT-4", "GMT-8", "0000"),
    ("0400", "GMT-3", "GMT-8", "2300-"),
    ("0200", "GMT-3", "GMT-8", "2100-"),
    ("2000", "GMT+4", "GMT+8", "0000+"),
    ("2000", "GMT+3", "GMT+8", "0100+"),
    ("2200", "GMT+3", "GMT+8", "0300+"),
]


@pytest.mark.parametrize("time,timezone_in,timezone_out,result", convert_across_timezone_data)
def test_convert_across_timezone(time, timezone_in, timezone_out, result):
    assert convert_time_across_timezones(time, timezone_in, timezone_out) == result
