import re

abbreviation_dict = {
    "mon": "MONDAY",
    "tue": "TUESDAY",
    "wed": "WEDNESDAY",
    "thu": "THURSDAY",
    "fri": "FRIDAY",
    "sat": "SATURDAY",
    "sun": "SUNDAY"
}
__day_regex = re.compile(r"((?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day|\b(?:mon|tue|tues|wed|thurs|thu|thur|fri|sat|sun)\b)", flags=re.IGNORECASE)

def parse_day(text):
    return set([abbreviation_to_day(i) for i in re.findall(__day_regex, text)])

def abbreviation_to_day(text):
    for key, value in abbreviation_dict.items():
        if re.search(key, text, re.IGNORECASE):
            return value