import re


__military_time_regex = re.compile(r"\b(?P<start>(?:2[0-3]|[0-1][0-9]):?(?:00|15|30|45))(?:\s?(?:-|to)\s?)?(?P<end>(?:2[0-3]|[0-1][0-9]):?(?:00|15|30|45))?\b", flags=re.IGNORECASE)
__double_period_time_regex = re.compile(r"(?P<start>(?:1[0-2]|0?[0-9])[:.]?(?:00|15|30|45)?)\s?(?P<period_start>[ap])\.?(?:m(?=-)|(?=-)|m\b|\b)\.?(?:\s?(?:-|to)\s?)?(?P<end>(?:1[0-2]|0?[0-9])[:.]?(?:00|15|30|45)?)?(?(end)\s?(?P<period_end>[ap])\.?m?\b)", flags=re.IGNORECASE)
__single_period_time_regex = re.compile(r"(?P<start>(?:1[0-2]|0?[0-9])[:.]?(?:00|15|30|45)?)(?:\s?(?:-|to)\s?)(?P<end>(?:1[0-2]|0?[0-9])[:.]?(?:00|15|30|45)?)\s?(?P<period>[ap])\.?m?\b", re.IGNORECASE)


def parse_time(text: str) -> (str, str):

    text = re.sub(r"\bnoon\b", "1200", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmidnight\b", "0000", text, flags=re.IGNORECASE)
    # this handles times in 7 - 11:45pm format
    single_period_match = re.search(__single_period_time_regex, text)
    if single_period_match and single_period_match.group("start") and single_period_match.group("end") and single_period_match.group("period"):
        end_period = single_period_match.group("period")
        mil_start = to_military_time(single_period_match.group("start"), end_period)
        mil_end = to_military_time(single_period_match.group("end"), end_period)

        if end_period.upper() == "P" and int(mil_start) > int(mil_end):
            mil_start = to_military_time(single_period_match.group("start"), "A")
        elif end_period.upper() == "A" and int(mil_start) > int(mil_end):
            mil_start = to_military_time(single_period_match.group("start"), "P")

        return (mil_start, mil_end)

    # this handles times in 7 am or 11:45pm or 7am - 11:45pm format
    double_period_match = re.search(__double_period_time_regex, text)
    if double_period_match and double_period_match.group("start") and double_period_match.group("period_start"):
        mil_start = to_military_time(double_period_match.group("start"), double_period_match.group("period_start"))
        mil_end = None
        if double_period_match.group("end") and double_period_match.group("period_end"):
            mil_end = to_military_time(double_period_match.group("end"), double_period_match.group("period_end"))
        return (mil_start, mil_end)

    # this handles times in 0000 or 2345 or 0000 - 2345 format
    military_time_match = re.search(__military_time_regex, text)
    if military_time_match:
        return (military_time_match.group("start").replace(":", ""), military_time_match.group("end").replace(":", "") if military_time_match.group("end") else None)

    return (None, None)


def to_military_time(time: str, period: chr) -> str:
    hours = -1
    minutes = -1
    m = re.match(r'(1[0-2]|0?[0-9])[:.]?(00|15|30|45)?', time, re.IGNORECASE)
    if m:
        hours = int(m.group(1))
        if (m.group(2)):
            minutes = int(m.group(2))
        else:
            minutes = 0

        if period.upper() == "P" and hours != 12:
            hours += 12

        if period.upper() == "A" and hours == 12:
            hours = 0

    if hours == -1 or minutes == -1:
        return None

    return f"{hours:02d}{minutes:02d}"
