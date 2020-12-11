import re
import typing


abbreviation_dict = {
    "weekday": ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"],
    "weekend": ["SATURDAY", "SUNDAY"],
    "mon": ["MONDAY"],
    "tue": ["TUESDAY"],
    "wed": ["WEDNESDAY"],
    "thu": ["THURSDAY"],
    "fri": ["FRIDAY"],
    "sat": ["SATURDAY"],
    "sun": ["SUNDAY"]
}
__day_regex = re.compile(r"((?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day|\b(?:mon|tue|tues|wed|thurs|thu|thur|fri|sat|sun)\b|week(?:day|end))", flags=re.IGNORECASE)


def parse_day(text: str) -> typing.Set[str]:
    days = []
    for day in re.findall(__day_regex, text):
        days.extend(abbreviation_to_day(day))
    return set(days)


def abbreviation_to_day(text: str) -> str:
    for key, value in abbreviation_dict.items():
        if re.search(key, text, re.IGNORECASE):
            return value


def sort_days(days: typing.Set[str]) -> typing.List[str]:
    days_sorted = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
    if days:
        return [day.capitalize() for day in days_sorted if day in days]
    return None
